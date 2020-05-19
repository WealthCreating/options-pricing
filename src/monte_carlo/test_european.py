#!/usr/bin/env python3
"""
Usage: test_options.py

Tests Monte Carlo simulations for pricing options.
"""

import unittest

import monte_carlo.options as options


class TestMonteCarlo(unittest.TestCase):
    """
    Unit test for Monte Carlo calculations for option prices.
    """
    def test_mc_euro_option(self):
        """
        Tests Monte Carlo simulations for calculating European options.
        """
        number_of_paths = 10000
        seed = 1234

        strike = 15
        expiry = 0.25
        spot = 30.14
        vol = 0.332
        r = 0.01
        price = options.CalcEuropeanOption.call_price(strike, expiry, spot,
                                                      vol, r, number_of_paths,
                                                      seed)
        print("Option Call Price (using Monte Carlo) is: {}".format(price))
        self.assertAlmostEqual(price, 15.195389688817, places=10)

        strike = 30
        expiry = 0.25
        spot = 30.14
        vol = 0.332
        r = 0.01
        price = options.CalcEuropeanOption.put_price(strike, expiry, spot, vol,
                                                     r, number_of_paths, seed)
        print("Option Put Price (using Monte Carlo) is: {}".format(price))
        self.assertAlmostEqual(price, 1.8925888827916253, places=10)


if __name__ == '__main__':
    unittest.main()
