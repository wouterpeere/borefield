"""
This file contains the base class for the ground classes.
"""
import abc
from abc import ABC
from GHEtool.VariableClasses.BaseClass import BaseClass


class GroundDataBaseClass(BaseClass, ABC):
    """
    Contains information regarding the ground data of the borefield.
    """

    __slots__ = 'k_s', 'volumetric_heat_capacity', 'alpha'

    def __init__(self, k_s: float = None,
                 volumetric_heat_capacity: float = 2.4 * 10**6):
        """

        Parameters
        ----------
        k_s : float
            Ground thermal conductivity [W/mK]
        volumetric_heat_capacity : float
            The volumetric heat capacity of the ground [J/m3K]
        """

        self.k_s = k_s  # W/mK
        self.volumetric_heat_capacity = volumetric_heat_capacity  # J/m3K
        if self.volumetric_heat_capacity is None or self.k_s is None:
            self.alpha = None
        else:
            self.alpha = self.k_s / self.volumetric_heat_capacity  # m2/s

    @abc.abstractmethod
    def calculate_Tg(self) -> float:
        """
        This function gives back the ground temperature

        Returns
        -------
        Tg : float
            Ground temperature [deg C]
        """

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for i in self.__slots__:
            if getattr(self, i) != getattr(other, i):
                return False
        return True
