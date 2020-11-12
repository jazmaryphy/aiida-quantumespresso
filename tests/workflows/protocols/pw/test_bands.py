# -*- coding: utf-8 -*-
"""Tests for the ``PwBandsWorkChain.get_builder_from_protocol`` method."""
import pytest

from aiida.engine import ProcessBuilder

from aiida_quantumespresso.common.types import ElectronicType, SpinType
from aiida_quantumespresso.workflows.pw.bands import PwBandsWorkChain


def test_default(fixture_code, generate_structure, data_regression, serialize_builder):
    """Test ``PwBandsWorkChain.get_builder_from_protocol`` for the default protocol."""
    code = fixture_code('quantumespresso.pw')
    structure = generate_structure()
    builder = PwBandsWorkChain.get_builder_from_protocol(code, structure)

    assert isinstance(builder, ProcessBuilder)
    data_regression.check(serialize_builder(builder))


def test_electronic_type(fixture_code, generate_structure):
    """Test ``PwBandsWorkChain.get_builder_from_protocol`` with ``electronic_type`` keyword."""
    code = fixture_code('quantumespresso.pw')
    structure = generate_structure()

    with pytest.raises(NotImplementedError):
        for electronic_type in [ElectronicType.AUTOMATIC]:
            PwBandsWorkChain.get_builder_from_protocol(code, structure, electronic_type=electronic_type)

    builder = PwBandsWorkChain.get_builder_from_protocol(code, structure, electronic_type=ElectronicType.INSULATOR)

    for namespace in [builder.relax['base'], builder.scf, builder.bands]:
        parameters = namespace['pw']['parameters'].get_dict()
        assert parameters['SYSTEM']['occupations'] == 'fixed'
        assert 'degauss' not in parameters['SYSTEM']
        assert 'smearing' not in parameters['SYSTEM']


def test_spin_type(fixture_code, generate_structure):
    """Test ``PwBandsWorkChain.get_builder_from_protocol`` with ``spin_type`` keyword."""
    code = fixture_code('quantumespresso.pw')
    structure = generate_structure()

    with pytest.raises(NotImplementedError):
        for spin_type in [SpinType.NON_COLLINEAR, SpinType.SPIN_ORBIT]:
            PwBandsWorkChain.get_builder_from_protocol(code, structure, spin_type=spin_type)

    builder = PwBandsWorkChain.get_builder_from_protocol(code, structure, spin_type=SpinType.COLLINEAR)

    for namespace in [builder.relax['base'], builder.scf, builder.bands]:
        parameters = namespace['pw']['parameters'].get_dict()
        assert parameters['SYSTEM']['nspin'] == 2
        assert parameters['SYSTEM']['starting_magnetization'] == {'Si': 0.1}