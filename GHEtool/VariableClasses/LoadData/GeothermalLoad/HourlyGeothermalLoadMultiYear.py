from __future__ import annotations

import warnings

import numpy as np

from typing import TYPE_CHECKING
from GHEtool.logger import ghe_logger
from GHEtool.VariableClasses.LoadData.GeothermalLoad.HourlyGeothermalLoad import HourlyGeothermalLoad

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


class HourlyGeothermalLoadMultiYear(HourlyGeothermalLoad):
    """
    This class contains all the information for geothermal load data with a monthly resolution and absolute input.
    This means that the inputs are both in kWh/month and kW/month.
    """

    def __init__(self, heating_load: ArrayLike | None = None, cooling_load: ArrayLike | None = None):
        """

        Parameters
        ----------
        heating_load : np.ndarray, list, tuple
            Heating load [kWh/h]
        cooling_load : np.ndarray, list, tuple
            Cooling load [kWh/h]
        """

        super().__init__()

        # initiate variables
        self._hourly_heating_load: np.ndarray = np.zeros(8760)
        self._hourly_cooling_load: np.ndarray = np.zeros(8760)

        # set variables
        heating_load = np.zeros(8760) if heating_load is None and cooling_load is None else heating_load
        self.hourly_heating_load = np.zeros_like(cooling_load) if heating_load is None else np.array(heating_load)
        self.hourly_cooling_load = np.zeros_like(heating_load) if cooling_load is None else np.array(cooling_load)

    def _check_input(self, load_array: ArrayLike) -> bool:
        """
        This function checks whether the input is valid or not.
        The input is correct if and only if:
        1) the input is a np.ndarray, list or tuple
        2) the length of the input is 8760
        3) the input does not contain any negative values.

        Parameters
        ----------
        load_array : np.ndarray, list or tuple

        Returns
        -------
        bool
            True if the inputs are valid
        """
        if not isinstance(load_array, (np.ndarray, list, tuple)):
            ghe_logger.error("The load should be of type np.ndarray, list or tuple.")
            return False
        if not len(load_array) % 8760 == 0:
            ghe_logger.error("The input data is not a multiple of 8760 hours")
            return False
        if np.min(load_array) < 0:
            ghe_logger.error("No value in the load can be smaller than zero.")
            return False
        return True

    @property
    def hourly_heating_load(self) -> np.ndarray:
        """
        This function returns the hourly heating load in kWh/h.

        Returns
        -------
        hourly heating : np.ndarray
            Hourly heating values [kWh/h] for one year, so the length of the array is 8760
        """
        return np.mean(self._hourly_heating_load.reshape((self.simulation_period, 8760)), axis=0)

    @hourly_heating_load.setter
    def hourly_heating_load(self, load: ArrayLike) -> None:
        """
        This function sets the hourly heating load [kWh/h] after it has been checked.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Hourly heating [kWh/h]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 8760, the input is not of the correct type, or it contains negative
            values
        """
        if self._check_input(load):
            self._hourly_heating_load = load
            self.simulation_period = int(len(load) / 8760)
            return
        raise ValueError

    @property
    def hourly_cooling_load(self) -> np.ndarray:
        """
        This function returns the hourly cooling load in kWh/h.

        Returns
        -------
        hourly cooling : np.ndarray
            Hourly cooling values [kWh/h] for one year, so the length of the array is 8760
        """
        return np.mean(self._hourly_cooling_load.reshape((self.simulation_period, 8760)), axis=0)

    @hourly_cooling_load.setter
    def hourly_cooling_load(self, load: ArrayLike) -> None:
        """
        This function sets the hourly cooling load [kWh/h] after it has been checked.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Hourly cooling [kWh/h]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 8760, the input is not of the correct type, or it contains negative
            values
        """
        if self._check_input(load):
            self._hourly_cooling_load = load
            self.simulation_period = int(len(load) / 8760)
            return
        raise ValueError

    @property
    def hourly_cooling_load_simulation_period(self) -> np.ndarray:
        """
        This function returns the hourly cooling in kWh/h for a whole simulation period.

        Returns
        -------
        hourly cooling : np.ndarray
            hourly cooling for the whole simulation period
        """
        return self._hourly_cooling_load

    @property
    def hourly_heating_load_simulation_period(self) -> np.ndarray:
        """
        This function returns the hourly heating in kWh/h for a whole simulation period.

        Returns
        -------
        hourly heating : np.ndarray
            hourly heating for the whole simulation period
        """
        return self._hourly_heating_load

    def __eq__(self, other) -> bool:
        if not isinstance(other, HourlyGeothermalLoad):
            return False
        if not np.array_equal(self._hourly_cooling_load, other._hourly_cooling_load):
            return False
        if not np.array_equal(self._hourly_heating_load, other._hourly_heating_load):
            return False
        if not self.simulation_period == other.simulation_period:
            return False
        return True

    def __add__(self, other):
        if isinstance(other, HourlyGeothermalLoadMultiYear):
            if self.simulation_period != other.simulation_period:
                raise ValueError("Cannot combine HourlyGeothermalLoadMultiYear classes with different simulation periods.")

            return HourlyGeothermalLoadMultiYear(self._hourly_heating_load + other._hourly_heating_load, self._hourly_cooling_load + other._hourly_cooling_load)

        if isinstance(other, HourlyGeothermalLoad):
            warnings.warn(
                "You combine a hourly load with a multi-year load. The result will be a multi-year load with" " the same simulation period as before."
            )
            return HourlyGeothermalLoadMultiYear(
                self._hourly_heating_load + np.tile(other.hourly_heating_load, self.simulation_period),
                self._hourly_cooling_load + np.tile(other.hourly_cooling_load, self.simulation_period),
            )

        try:
            return other.__add__(self)
        except TypeError:  # pragma: no cover
            raise TypeError("Cannot perform addition. Please check if you use correct classes.")  # pragma: no cover
