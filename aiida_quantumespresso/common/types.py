# -*- coding: utf-8 -*-
"""Module with common data types."""
import enum


class ElectronicType(enum.Enum):
    """Enumeration to inidicate the electronic type of a system."""

    METAL = 'metal'
    INSULATOR = 'insulator'
    AUTOMATIC = 'automatic'
