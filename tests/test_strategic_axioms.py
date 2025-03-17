"""
    File: test_strategic_axioms.py
    Author: Devin AI
    Date: March 17, 2025
    
    Tests for strategic axioms
"""

import unittest
from pref_voting.profiles import Profile
from pref_voting.profiles_with_ties import ProfileWithTies
from pref_voting.strategic_axioms import (
    strategy_proofness,
    truncation_strategy_proofness,
    has_strategy_proofness_violation,
    find_all_strategy_proofness_violations,
    has_truncation_strategy_proofness_violation,
    find_all_truncation_strategy_proofness_violations
)
from pref_voting.other_methods import plurality
from pref_voting.scoring_methods import borda
from pref_voting.margin_based_methods import split_cycle

class TestStrategicAxioms(unittest.TestCase):
    
    def test_truncation_strategy_proofness_with_profile(self):
        """Test truncation_strategy_proofness with a Profile object."""
        
        # Create a profile where truncation can benefit a voter
        prof = Profile(
            [[0, 1, 2], [0, 1, 2], [2, 1, 0], [2, 1, 0], [1, 0, 2]]
        )
        
        # Test has_truncation_strategy_proofness_violation
        self.assertTrue(has_truncation_strategy_proofness_violation(prof, plurality))
        
        # Test find_all_truncation_strategy_proofness_violations
        violations = find_all_truncation_strategy_proofness_violations(prof, plurality)
        self.assertTrue(len(violations) > 0)
        
        # Create a profile where truncation cannot benefit a voter
        prof2 = Profile(
            [[0, 1, 2], [0, 1, 2], [0, 1, 2], [1, 0, 2], [1, 0, 2]]
        )
        
        # Test has_truncation_strategy_proofness_violation
        self.assertFalse(has_truncation_strategy_proofness_violation(prof2, plurality))
        
        # Test find_all_truncation_strategy_proofness_violations
        violations = find_all_truncation_strategy_proofness_violations(prof2, plurality)
        self.assertEqual(len(violations), 0)
    
    def test_truncation_strategy_proofness_with_profile_with_ties(self):
        """Test truncation_strategy_proofness with a ProfileWithTies object."""
        
        # Create a profile with ties where truncation can benefit a voter
        prof = ProfileWithTies(
            [{0: 1, 1: 2, 2: 3}, {0: 1, 1: 2, 2: 3}, {2: 1, 1: 2, 0: 3}, {2: 1, 1: 2, 0: 3}, {1: 1, 0: 2, 2: 3}]
        )
        
        # Test has_truncation_strategy_proofness_violation
        self.assertTrue(has_truncation_strategy_proofness_violation(prof, plurality))
        
        # Test find_all_truncation_strategy_proofness_violations
        violations = find_all_truncation_strategy_proofness_violations(prof, plurality)
        self.assertTrue(len(violations) > 0)
        
        # Create a profile with ties where truncation cannot benefit a voter
        prof2 = ProfileWithTies(
            [{0: 1, 1: 2, 2: 3}, {0: 1, 1: 2, 2: 3}, {0: 1, 1: 2, 2: 3}, {1: 1, 0: 2, 2: 3}, {1: 1, 0: 2, 2: 3}]
        )
        
        # Test has_truncation_strategy_proofness_violation
        self.assertFalse(has_truncation_strategy_proofness_violation(prof2, plurality))
        
        # Test find_all_truncation_strategy_proofness_violations
        violations = find_all_truncation_strategy_proofness_violations(prof2, plurality)
        self.assertEqual(len(violations), 0)
    
    def test_truncation_strategy_proofness_with_different_voting_methods(self):
        """Test truncation_strategy_proofness with different voting methods."""
        
        # Create a profile
        prof = Profile(
            [[0, 1, 2], [0, 1, 2], [2, 1, 0], [2, 1, 0], [1, 0, 2]]
        )
        
        # Test with plurality
        self.assertTrue(has_truncation_strategy_proofness_violation(prof, plurality))
        
        # Test with borda
        borda_violations = has_truncation_strategy_proofness_violation(prof, borda)
        
        # Test with split_cycle
        split_cycle_violations = has_truncation_strategy_proofness_violation(prof, split_cycle)
    
    def test_truncation_strategy_proofness_with_different_set_preferences(self):
        """Test truncation_strategy_proofness with different set preferences."""
        
        # Create a profile
        prof = Profile(
            [[0, 1, 2], [0, 1, 2], [2, 1, 0], [2, 1, 0], [1, 0, 2]]
        )
        
        # Test with single-winner
        single_winner_violations = has_truncation_strategy_proofness_violation(prof, plurality, set_preference="single-winner")
        
        # Test with weak-dominance
        weak_dominance_violations = has_truncation_strategy_proofness_violation(prof, plurality, set_preference="weak-dominance")
        
        # Test with optimist
        optimist_violations = has_truncation_strategy_proofness_violation(prof, plurality, set_preference="optimist")
        
        # Test with pessimist
        pessimist_violations = has_truncation_strategy_proofness_violation(prof, plurality, set_preference="pessimist")
    
    def test_axiom_instances(self):
        """Test the axiom instances."""
        
        # Test strategy_proofness
        self.assertEqual(strategy_proofness.name, "Strategy Proofness")
        self.assertEqual(strategy_proofness.has_violation, has_strategy_proofness_violation)
        self.assertEqual(strategy_proofness.find_all_violations, find_all_strategy_proofness_violations)
        
        # Test truncation_strategy_proofness
        self.assertEqual(truncation_strategy_proofness.name, "Truncation Strategy Proofness")
        self.assertEqual(truncation_strategy_proofness.has_violation, has_truncation_strategy_proofness_violation)
        self.assertEqual(truncation_strategy_proofness.find_all_violations, find_all_truncation_strategy_proofness_violations)

if __name__ == "__main__":
    unittest.main()
