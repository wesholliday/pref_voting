'''
    File: test_probabilistic_methods.py
    Author: Wes Holliday (wesholliday@berkeley.edu) and Eric Pacuit (epacuit@umd.edu)
    Date: April 14, 2024

    Tests for probabilistic voting methods.
'''

import pytest
import random
from pref_voting import Profile
from pref_voting.probabilistic_methods import random_consensus_builder

def test_random_consensus_builder():
    """Test the random consensus builder voting method"""

    # Create a simple profile with 3 voters and 3 candidates
    prof = Profile([[0, 1, 2], [1, 2, 0], [2, 0, 1]], [1, 1, 1])

    # Set random seed for reproducibility
    random.seed(42)

    # Test with different beta values
    result1 = random_consensus_builder(prof, beta=0.6)
    assert sum(result1.values()) == 1.0  # Probabilities should sum to 1
    assert all(p >= 0 and p <= 1 for p in result1.values())  # Valid probabilities

    result2 = random_consensus_builder(prof, beta=0.9)
    assert sum(result2.values()) == 1.0
    assert all(p >= 0 and p <= 1 for p in result2.values())

    # Test with restricted candidate set
    curr_cands = [0, 1]
    result3 = random_consensus_builder(prof, curr_cands=curr_cands, beta=0.6)
    assert sum(result3.values()) == 1.0
    assert all(c in curr_cands for c in result3.keys())

    # Test edge cases
    empty_prof = Profile([], [])
    result4 = random_consensus_builder(empty_prof)
    assert sum(result4.values()) == 1.0

    result5 = random_consensus_builder(prof, curr_cands=[])
    assert result5 == {}

    # Test that the method handles different voter counts correctly
    prof2 = Profile([[0, 1, 2], [1, 2, 0]], [2, 3])  # 5 voters total
    result6 = random_consensus_builder(prof2, beta=0.6)
    assert sum(result6.values()) == 1.0
