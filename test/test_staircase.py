""" Unit tests for Staircase class. 

    Written by: Travis M. Moore
    Created: December 13, 2023
    Last edited: December 14, 2023
"""

###########
# Imports #
###########
# Import testing packages
from unittest import TestCase
from unittest import mock

# Import data science packages
import numpy as np
import pandas as pd

# Import custom modules
from models import staircase


#########
# Begin #
#########
class TestStaircase(TestCase):
    def setUp(self):
        """ Create Staircase.
        """
        # Create staircase
        self.s = staircase.Staircase(
            start_val=60,
            step_sizes=[8,4],
            nUp=1,
            nDown=2,
            nTrials=10,
            nReversals=2,
            rapid_descend=True,
            min_val=50,
            max_val=80
        )


    def tearDown(self):
        del self.s


    ##############
    # Unit Tests #
    ##############
    def test_staircase_parameters_on_init(self):
        """ Test that arguments are assigned correctly.
        """
        self.assertEqual(self.s.current_level, 60)
        self.assertEqual(self.s.step_sizes, [8,4])
        self.assertEqual(self.s.nUp, 1)
        self.assertEqual(self.s.nDown, 2)
        self.assertEqual(self.s.nTrials, 10)
        self.assertEqual(self.s.nReversals, 2)
        self.assertEqual(self.s.rapid_descend, True)
        self.assertEqual(self.s.min_val, 50)
        self.assertEqual(self.s.max_val, 80)


    def test_staircase_default_attributes_on_init(self):
        """ Test that public attribute defaults are correct.
        """
        self.assertEqual(self.s.scores, [])
        self.assertEqual(self.s.reversals, {})
        self.assertEqual(self.s._level_tracker, [])
        self.assertEqual(self.s.levels, [])
        self.assertEqual(self.s._step_index, 0)
        self.assertEqual(self.s._trial_num, 0)


    def test__handle_response_one_correct(self):
        # Add response to staircase
        response = 1
        self.s._handle_response(response)

        # Assertions
        self.assertEqual(self.s.scores, [1])
        self.assertEqual(self.s._level_tracker, [1])


    def test__handle_response_two_correct(self):
        # Add two correct responses to staircase
        responses = [1, 1]
        for response in responses:
            self.s._handle_response(response)

        # Assertions
        self.assertEqual(self.s.scores, [1, 1])
        self.assertEqual(self.s._level_tracker, [1, 1])


    def test__handle_response_one_incorrect(self):
        # Add response to staircase
        response = -1
        self.s._handle_response(response)

        # Assertions
        self.assertEqual(self.s.scores, [-1])
        self.assertEqual(self.s._level_tracker, [-1])


    def test__handle_response_two_incorrect(self):
        # Add two incorrect responses to staircase
        responses = [-1, -1]
        for response in responses:
            self.s._handle_response(response)

        # Assertions
        self.assertEqual(self.s.scores, [-1, -1])
        self.assertEqual(self.s._level_tracker, [-1, -1])


    def test__calc_reversals_1(self):
        # Update scores attribute
        self.s.scores = [1, 1, -1]
        self.s._calc_reversals()

        # Assertions
        self.assertEqual(len(self.s.reversals), 1)
        self.assertEqual(self.s.reversals, {0:60})


    def test__calc_reversals_2(self):
        # Update scores attribute
        self.s.scores = [-1, 1, 1]
        self.s._calc_reversals()

        # Assertions
        self.assertEqual(len(self.s.reversals), 1)
        self.assertEqual(self.s.reversals, {0:60})


    def test__calc_reversals_all_correct(self):
        # Update scores attribute
        self.s.scores = [1, 1, 1]
        self.s._calc_reversals()

        # Assertions
        self.assertEqual(len(self.s.reversals), 0)
        self.assertEqual(self.s.reversals, {})


    def test__calc_reversals_all_incorrect(self):
        # Update scores attribute
        self.s.scores = [-1, -1, -1]
        self.s._calc_reversals()

        # Assertions
        self.assertEqual(len(self.s.reversals), 0)
        self.assertEqual(self.s.reversals, {})


    def test__calc_reversals_none_1(self):
        # Update scores attribute
        self.s.scores = [-1, 1, -1]
        self.s._calc_reversals()

        # Assertions
        self.assertEqual(len(self.s.reversals), 0)
        self.assertEqual(self.s.reversals, {})


    def test__calc_reversals_none_2(self):
        # Update scores attribute
        self.s.scores = [1, -1, 1]
        self.s._calc_reversals()

        # Assertions
        self.assertEqual(len(self.s.reversals), 0)
        self.assertEqual(self.s.reversals, {})













    def test_increase_trial_num(self):
        self.assertEqual(self.s._trial_num, 0)
        self.s._increase_trial_num()
        self.assertEqual(self.s._trial_num, 1)


    #####################
    # Integration Tests #
    #####################
    def test_add_response_one_correct(self):
        # Add one correct response to staircase
        response = 1
        self.s.add_response(response)

        # Assertions
        self.assertEqual(self.s.levels, [60])
        self.assertEqual(self.s.scores, [1])
        self.assertEqual(self.s._level_tracker, [1])


    def test_add_response_two_correct(self):
        # Add two correct responses
        responses = [1, 1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.levels, [60, 60])
        self.assertEqual(self.s.scores, [1, 1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [])

        # The current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 52)

        # No reversals should have occurred
        self.assertDictEqual(self.s.reversals, {})


    def test_add_response_three_correct(self):
        # Add three correct responses
        responses = [1, 1, 1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.levels, [60, 60, 52])
        self.assertEqual(self.s.scores, [1, 1, 1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [1])

        # The current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 52)

        # No reversals should have occurred
        self.assertDictEqual(self.s.reversals, {})


    def test_add_response_one_incorrect(self):
        # Add one incorrect response to staircase
        response = -1
        self.s.add_response(response)

        # Assertions
        # Current level
        self.assertEqual(self.s.levels, [60])

        # List of scores
        self.assertEqual(self.s.scores, [-1])

        # _level_tracker should reset after one incorrect response
        self.assertEqual(self.s._level_tracker, [])

        # No reversals should have occurred
        self.assertDictEqual(self.s.reversals, {})


    def test_add_response_two_incorrect(self):
        # Add two incorrect responses
        responses = [-1, -1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.levels, [60, 68])
        self.assertEqual(self.s.scores, [-1, -1])

        # _level_tracker should reset after one incorrect response
        self.assertEqual(self.s._level_tracker, [])

        # The next level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 76)

        # No reversals should have occurred
        self.assertDictEqual(self.s.reversals, {})


    def test_correct_incorrect_reversal(self):
        # Add two correct responses and one incorrect response
        responses = [1, 1, -1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.levels, [60, 60, 52])
        self.assertEqual(self.s.scores, [1, 1, -1])

        # _level_tracker should reset after one incorrect response
        self.assertEqual(self.s._level_tracker, [])

        # The  next current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 60)

        # One reversal should have occurred
        self.assertDictEqual(self.s.reversals, {2:52})


    def test_incorrect_correct_reversal(self):
        # Add one incorrect response and two correct responses
        responses = [-1, 1, 1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.levels, [60, 68, 68])
        self.assertEqual(self.s.scores, [-1, 1, 1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [])

        # The next current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 60)

        # One reversal should have occurred
        self.assertDictEqual(self.s.reversals, {2:68})


    def test_incorrect_correct_no_reversal(self):
        # Add one incorrect response and one correct response
        responses = [-1, 1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.levels, [60, 68])
        self.assertEqual(self.s.scores, [-1, 1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [1])

        # The next current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 68)

        # No reversals should have occurred
        self.assertDictEqual(self.s.reversals, {})


    def test_correct_incorrect_no_reversal(self):
        # Add one correct response and one incorrect response
        responses = [1, -1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.levels, [60, 60])
        self.assertEqual(self.s.scores, [1, -1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [])

        # The next current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 68)

        # No reversals should have occurred
        self.assertDictEqual(self.s.reversals, {})
