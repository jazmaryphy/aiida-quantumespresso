# -*- coding: utf-8 -*-
"""Tests for the ``PwBaseWorkChain.get_builder_from_protocol`` method."""
import pytest

from aiida.engine import ProcessBuilder

from aiida_quantumespresso.common.types import ElectronicType
from aiida_quantumespresso.workflows.pw.base import PwBaseWorkChain


def test_default(fixture_code, generate_structure, data_regression, serialize_builder):
    """Test ``PwBaseWorkChain.get_builder_from_protocol`` for the default protocol."""
    code = fixture_code('quantumespresso.pw')
    structure = generate_structure()
    builder = PwBaseWorkChain.get_builder_from_protocol(code, structure)

    assert isinstance(builder, ProcessBuilder)
    data_regression.check(serialize_builder(builder))


def test_electronic_type(fixture_code, generate_structure):
    """Test ``PwBaseWorkChain.get_builder_from_protocol`` with ``electronic_type`` keyword."""
    code = fixture_code('quantumespresso.pw')
    structure = generate_structure()

    with pytest.raises(NotImplementedError):
        for electronic_type in [ElectronicType.AUTOMATIC]:
            PwBaseWorkChain.get_builder_from_protocol(code, structure, electronic_type=electronic_type)

    builder = PwBaseWorkChain.get_builder_from_protocol(code, structure, electronic_type=ElectronicType.INSULATOR)
    parameters = builder.pw.parameters.get_dict()

    assert parameters['SYSTEM']['occupations'] == 'fixed'
    assert 'degauss' not in parameters['SYSTEM']
    assert 'smearing' not in parameters['SYSTEM']
