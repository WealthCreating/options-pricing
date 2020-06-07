"""Represents parameters used in Monte Carlo calculations."""

from abc import ABC, abstractmethod


class Parameters(ABC):
    """
    Base class for all parameters used in Monte Carlo calculations.

    Each parameter is a function (can be constant) of time.
    """

    @abstractmethod
    def integral(self, time1, time2):
        """
        Calculates an integral for the parameter (function) between two points in time.

        Args:
            time1 (float): Starting time point
            time2 (float): Ending time point

        Returns:
            float: Resulting integral value
        """

    @abstractmethod
    def integral_square(self, time1, time2):
        """
        Calculates an integral of the squared parameter (function) between two points
        in time.

        Args:
            time1 (float): Starting time point
            time2 (float): Ending time point

        Returns:
            float: Resulting integral value
        """


class ParametersConstant(Parameters):
    """
    Represents a constant parameter (function).
    """

    def __init__(self, constant) -> None:
        """
        Initializes the class with a constant value.

        Args:
            constant (float): Constant value to which the function is equal to.
        """
        self.constant = constant
        self.constant_square = constant * constant

    def integral(self, time1, time2):
        """
        Calculates an integral of a constant function between two points in time.

        Args:
            time1 (float): Starting time point
            time2 (float): Ending time point

        Returns:
            float: Resulting integral
        """
        return (time2 - time1) * self.constant

    def integral_square(self, time1, time2):
        """
        Calculates an integral of a squared constant function between two points in
        time.

        Args:
            time1 (float): Starting time point
            time2 (float): Ending time point

        Returns:
            float: Resulting integral
        """
        return (time2 - time1) * self.constant_square
