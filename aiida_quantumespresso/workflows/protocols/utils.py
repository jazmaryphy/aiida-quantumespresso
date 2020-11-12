# -*- coding: utf-8 -*-
"""Utilities to manipulate the workflow input protocols."""
import functools
import os
import pathlib
import yaml


def recursive_merge(left, right):
    """Recursively merge two dictionaries into a single dictionary.

    :param left: first dictionary
    :param right: second dictionary
    :return: the recursively merged dictionary
    """
    import collections

    for key, value in left.items():
        if key in right:
            if isinstance(value, collections.abc.Mapping) and isinstance(right[key], collections.abc.Mapping):
                right[key] = recursive_merge(value, right[key])

    merged = left.copy()
    merged.update(right)

    return merged


def get_protocol_inputs(cls, protocol=None, overrides=None):
    """Docs."""
    from aiida.plugins.entry_point import get_entry_point_from_class

    _, entry_point = get_entry_point_from_class(cls.__module__, cls.__name__)
    entry_point_name = entry_point.name
    parts = entry_point_name.split('.')
    parts.pop(0)
    filename = f'{parts.pop()}.yaml'
    basepath = functools.reduce(os.path.join, parts)

    with (pathlib.Path(__file__).resolve().parent / basepath / filename).open() as handle:
        data = yaml.safe_load(handle)

    protocol = protocol or data['default']
    inputs = recursive_merge(data['base'], data['protocols'][protocol])
    inputs.pop('description')

    if overrides:
        return recursive_merge(inputs, overrides)

    return inputs


def get_magnetization_parameters() -> dict:
    """Return the mapping of suggested initial magnetic moments for each element.

    :returns: the magnetization parameters.
    """
    with (pathlib.Path(__file__).resolve().parent / 'magnetization.yaml').open() as handle:
        return yaml.safe_load(handle)


def get_initial_magnetization(structure, pseudo_family):
    """Return the dictionary with initial magnetization for each kind in the structure.

    :param structure: the structure.
    :param pseudo_family: pseudopotential family.
    :returns: dictionary of initial magnetizations.
    """
    magnetic_parameters = get_magnetization_parameters()
    initial_magnetization = {}

    for kind in structure.kinds:
        magnetic_moment = magnetic_parameters[kind.symbol]['magmom']

        if magnetic_moment == 0:
            magnetic_moment = magnetic_parameters['default']
        else:
            z_valence = pseudo_family.get_pseudo(element=kind.symbol).z_valence
            magnetic_moment /= float(z_valence)

        initial_magnetization[kind.name] = magnetic_moment

    return initial_magnetization
