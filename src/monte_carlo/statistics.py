"""Accumulates statistics during Monte Carlo runs."""

import math
from abc import abstractmethod


class StatisticsMC:

    """
    Base class for all statistics accumulators.
    """

    @abstractmethod
    def dump_one_result(self, result):
        """


        Computes ongoing statistics based on an incoming result.

        Args:
            result (float): Incoming result.
        """

    @abstractmethod
    def get_results_so_far(self):
        """
        Returns statistics accumulated up to this point.

        Returns:
            (array[array[float]]): Computed statistics.
        """


class StatisticsMean(StatisticsMC):
    """
    Computes a running mean of incoming results.
    """

    def __init__(self):
        """
        Initializes a running sum and a number of calculated (done) paths.
        """
        self.running_sum = 0.0
        self.paths_done = 0

    def dump_one_result(self, result):
        """
        Given a new result computes a running sum and keeps track of how many paths are
        calculated to this point.

        Args:
            result (float): Incoming result.
        """
        self.running_sum += result
        self.paths_done += 1

    def get_results_so_far(self):
        return [[self.running_sum / self.paths_done]]


class ConvergenceTable(StatisticsMC):
    """
    Saves running statistics at discrete points in time.
    """

    def __init__(self, stats):
        """
        Initializes storage for keeping track of results. Also, defines a stopping point
        schedule.

        Args:
             stats (:obj:`StatisticsMC`): Particular class used to calculate running
                statistics.
        """
        self.stats = stats
        self.results_so_far = []
        self.stopping_point = 2
        self.paths_done = 0

    def dump_one_result(self, result):
        """
        Given a new result computes a running statistics and keeps track of how many
        paths were calculated so far. Also, at pre-defined stopping points, the latest
        statistic is saved into an array.

        Args:
            result (float): Incoming result.
        """
        self.stats.dump_one_result(result)
        self.paths_done += 1

        if self.paths_done == self.stopping_point:
            self.stopping_point = math.ceil(self.stopping_point * 2)

            this_result = self.stats.get_results_so_far()
            for i in range(len(this_result)):
                this_result[i].append(self.paths_done)
                self.results_so_far.append(this_result[i])

    def get_results_so_far(self):
        """
        Returns statistics results saved up to this point.

        Returns:
            (:obj:`array[array[float]]`): Saved results.
        """
        tmp = self.results_so_far.copy()

        if self.paths_done != self.stopping_point:
            this_result = self.stats.get_results_so_far()
            for i in range(len(this_result)):
                this_result[i].append(self.paths_done)
                tmp.append(this_result[i])

        return tmp
