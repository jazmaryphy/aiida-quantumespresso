# -*- coding: utf-8 -*-
"""Module with common data types."""
import enum


class ElectronicType(enum.Enum):
    """Enumeration to inidicate the electronic type of a system."""

    METAL = 'metal'
    INSULATOR = 'insulator'
    AUTOMATIC = 'automatic'


class SpinType(enum.Enum):
    """Enumeration to inidicate the spin polarization type of a system."""

    NONE = 'none'
    COLLINEAR = 'collinear'
    NON_COLLINEAR = 'non_collinear'
    SPIN_ORBIT = 'spin_orbit'
