"""Represents miscellaneous option types and Monte Carlo simulations."""

import math
import random
from abc import ABC, abstractmethod

from .parameters import ParametersConstant
from .statistics import ConvergenceTable, StatisticsMean


class PayOff(ABC):
    """
    Abstract representation for option payoff functions.
    """

    def __init__(self, strike):
        """
        Initializes a payoff class by defining a strike price.

        Args:
            strike (float): Given strike price
        """
        self.strike = strike

    @abstractmethod
    def calc(self, spot):
        """
        Performs a payoff calculation given a spot price.

        Args:
            spot (float): Given spot price.
        """


class PayOffCall(PayOff):
    """
    Represents a payoff function for a call option.
    """

    def calc(self, spot):
        """
        Calculates a payoff amount for a call option given a spot price.

        Args:
            spot (float): Spot price.

        Returns:
             (float): Resulting payoff amount.
        """
        return max(spot - self.strike, 0)


class PayOffPut(PayOff):
    """
    Represents a payoff function for a put option.
    """

    def calc(self, spot):
        """
        Calculates a payoff amount for a put option given a spot price.

        Args:
            spot (float): Spot price.

        Returns:
             (float): Resulting payoff amount.
        """
        return max(self.strike - spot, 0)


class PayOffDoubleDigital(PayOff):
    """
    Represents a payoff function for a double digital option.
    """

    def __init__(self, lower_level, upper_level):
        """
        Initializes lower and upper levels for a double digital option.

        Args:
            lower_level (float): Lower limit
            upper_level (float): Upper limit
        """
        self.lower_level = lower_level
        self.upper_level = upper_level

    def calc(self, spot):
        """
        Calculates a payoff amount for a double digital option given a spot price.

        Args:
            spot (float): Spot price.

        Returns:
             (float): Returns 0 if the spot price is below (inclusive) the lower level
                or above the upper level (inclusive).
        """
        if spot <= self.lower_level:
            return 0

        if spot >= self.upper_level:
            return 0

        return 1


class VanillaOption:
    """
    Describes a generic vanilla option (either put or call).
    """

    def __init__(self, expiry, pay_off):
        """
        Initializes an expiry and a payoff function.

        Args:
            expiry (float): Given expiry.
            pay_off (float): Given payoff function.
        """
        self.expiry = expiry
        self.pay_off = pay_off

    def get_expiry(self):
        """
        Returns the set expiry.

        Returns:
            (float): Set expiry.
        """
        return self.expiry

    def calc_pay_off(self, spot):
        """
        Calculates the payoff function for a given spot.

        Args:
            spot (float): A given spot.

        Returns:
            (float): The payoff amount.
        """
        return self.pay_off.calc(spot)


class Simulation:
    """
    Performs a Monte Carlo simulation for pricing options.
    """

    @staticmethod
    def option_price(option, spot, vol, r, number_of_paths, gatherer, seed):
        """
        Calculates an option price by running a Monte Carlo simulation.

        Args:
            option (float): Option type to use.
            spot (float): Spot price.
            vol (:obj:`Parameters`): Volatility function.
            r (:obj:`Parameters`): Interest rate function.
            number_of_paths (int): Number of random paths to generate.
            gatherer (:obj:`MCStatistics`): Interest rate function.
            seed (int): Random seed.

        Returns:
            (float): Resulting put price.
        """
        if seed is not None:
            random.seed(seed)

        expiry = option.get_expiry()
        variance = vol.integral_square(0, expiry)
        root_variance = math.sqrt(variance)
        ito_correction = -0.5 * variance
        moved_spot = spot * math.exp(r.integral(0, expiry) + ito_correction)
        discounting = math.exp(-r.integral(0, expiry))
        for _ in range(number_of_paths):
            this_gaussian = random.gauss(0, 1)
            this_spot = moved_spot * math.exp(root_variance * this_gaussian)
            this_payoff = option.calc_pay_off(this_spot)
            gatherer.dump_one_result(discounting * this_payoff)


class CalcEuropeanOption:
    """
    Calculates a European option using Monte Carlo methods.
    """

    @staticmethod
    def call_price_stats(strike, expiry, spot, vol, r, number_of_paths, seed=None):
        """
        Calculates a call price for a European option by running a Monte Carlo
        simulation.

        Args:
            strike (float): Strike price.
            expiry (float): Expiry.
            spot (float): Spot price.
            vol (:obj:`Parameters`): Volatility function.
            r (:obj:`Parameters`): Interest rate function.
            number_of_paths (int): Number of paths to calculate.
            seed (int): Random seed.

        Returns:
            (:obj:`ConvergenceTable`): Returns statistics gathered during
                the Monte Carlo run.
        """
        gatherer = ConvergenceTable(StatisticsMean())

        Simulation.option_price(
            VanillaOption(expiry, PayOffCall(strike)),
            spot,
            ParametersConstant(vol),
            ParametersConstant(r),
            number_of_paths,
            gatherer,
            seed,
        )
        return gatherer

    @staticmethod
    def call_price(strike, expiry, spot, vol, r, number_of_paths, seed=None):
        """
        Calculates a call price for a European option by running a Monte Carlo
        simulation.

        Args:
            strike (float): Strike price.
            expiry (float): Expiry.
            spot (float): Spot price.
            vol (:obj:`Parameters`): Volatility function.
            r (:obj:`Parameters`): Interest rate function.
            number_of_paths (int): Number of paths to calculate.
            seed (int): Random seed.

        Returns:
            (float): Resulting call price.
        """
        convergence_table = CalcEuropeanOption.call_price_stats(
            strike, expiry, spot, vol, r, number_of_paths, seed
        )
        price = convergence_table.get_results_so_far()[-1][0]
        return price

    @staticmethod
    def put_price_stats(strike, expiry, spot, vol, r, number_of_paths, seed=None):
        """
        Calculates a put price for a European option by running a Monte Carlo
        simulation.

        Args:
            strike (float): Strike price.
            expiry (float): Expiry.
            spot (float): Spot price.
            vol (:obj:`Parameters`): Volatility function.
            r (:obj:`Parameters`): Interest rate function.
            number_of_paths (int): Number of paths to calculate.
            seed (int): Random seed.

        Returns:
            (:obj:`ConvergenceTable`): Returns statistics gathered during the Monte
                Carlo run.
        """
        gatherer = ConvergenceTable(StatisticsMean())

        Simulation.option_price(
            VanillaOption(expiry, PayOffPut(strike)),
            spot,
            ParametersConstant(vol),
            ParametersConstant(r),
            number_of_paths,
            gatherer,
            seed,
        )
        return gatherer

    @staticmethod
    def put_price(strike, expiry, spot, vol, r, number_of_paths, seed=None):
        """
        Calculates a put price for a European option by running a Monte Carlo
        simulation.

        Args:
            strike (float): Strike price.
            expiry (float): Expiry.
            spot (float): Spot price.
            vol (:obj:`Parameters`): Volatility function.
            r (:obj:`Parameters`): Interest rate function.
            number_of_paths (int): Number of paths to calculate.
            seed (int): Random seed.

        Returns:
            (float): Resulting put price.
        """
        convergence_table = CalcEuropeanOption.put_price_stats(
            strike, expiry, spot, vol, r, number_of_paths, seed
        )
        price = convergence_table.get_results_so_far()[-1][0]
        return price
