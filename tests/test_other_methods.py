from pref_voting.other_methods import *
from pref_voting.profiles import Profile
import pytest

@pytest.mark.parametrize("voting_method, expected", [
    (absolute_majority, {
        'condorcet_cycle': [], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1]
    }),
    (pareto, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0, 1, 2], 
        'linear_profile_0_curr_cands': [1, 2]
    }),
    (kemeny_young, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1]
    }),
    (bucklin, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1]
    }),
    (simplified_bucklin, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1]
    }),
    (weighted_bucklin, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1]
    }),
    (superior_voting, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1]
    })
])
def test_other_methods(
    voting_method, 
    expected, 
    condorcet_cycle, 
    linear_profile_0):
    assert voting_method(condorcet_cycle) == expected['condorcet_cycle']
    assert voting_method(linear_profile_0) == expected['linear_profile_0']
    if 'linear_profile_0_curr_cands' in expected:
        assert voting_method(linear_profile_0, curr_cands=[1, 2]) == expected['linear_profile_0_curr_cands']


def test_pareto(): 
    prof = Profile([[0, 1, 2], [0, 2, 1], [2, 0, 1]])
    assert pareto(prof) == [0, 2]

    prof = ProfileWithTies([
        {0:1, 1:1},
        {0:1, 1:1, 2:2}
    ])
    curr_using_extended_strict_preference = prof.using_extended_strict_preference
    assert pareto(prof, use_extended_strict_preferences=False) == [0, 1, 2]
    assert prof.using_extended_strict_preference == curr_using_extended_strict_preference

    curr_using_extended_strict_preference = prof.using_extended_strict_preference
    assert pareto(prof, use_extended_strict_preferences=True) == [0, 1]
    assert prof.using_extended_strict_preference == curr_using_extended_strict_preference

def test_bracket(condorcet_cycle, linear_profile_0):
    assert bracket_voting(condorcet_cycle, seed=42) == [2]
    assert bracket_voting(linear_profile_0) == [0]
    assert bracket_voting(linear_profile_0, curr_cands=[1, 2]) == [1]


def test_bucklin_with_explanation(condorcet_cycle, linear_profile_0):
    ws, exp = bucklin_with_explanation(condorcet_cycle)
    assert ws == [0, 1, 2]
    assert exp == {0: 2, 1: 2, 2: 2}
    ws, exp = bucklin_with_explanation(linear_profile_0)
    assert ws == [0]
    assert exp ==  {0: 2, 1: 0, 2: 1}
    prof = Profile([[0, 1, 2], [0, 1, 2], [1, 2, 0], [2, 1, 0]])
    ws, exp = bucklin_with_explanation(prof)
    assert ws == [1]
    assert exp == {0: 2, 1: 4, 2: 2}


def test_simplified_bucklin_with_explanation(condorcet_cycle, linear_profile_0):
    ws, exp = simplified_bucklin_with_explanation(condorcet_cycle)
    assert ws == [0, 1, 2]
    assert exp == {0: 2, 1: 2, 2: 2}
    ws, exp = simplified_bucklin_with_explanation(linear_profile_0)
    assert ws == [0]
    assert exp ==  {0: 2, 1: 0, 2: 1}
    prof = Profile([[0, 1, 2], [0, 1, 2], [1, 2, 0], [2, 1, 0]])
    ws, exp = simplified_bucklin_with_explanation(prof)
    assert ws == [1]
    assert exp == {0: 2, 1: 4, 2: 2}


def test_kemeny_young_rankings(condorcet_cycle, linear_profile_0):
    assert kemeny_young_rankings(condorcet_cycle) == ([(0, 1, 2), (1, 2, 0), (2, 0, 1)],4)
    assert kemeny_young_rankings(linear_profile_0) == ([(0, 1, 2)], 3)


def is_special_case_profile(profile):
    """Check if the profile is one of the special cases from Brandt's paper.
    
    Returns:
        tuple: (is_special_case, expected_winners, expected_scores)
    """
    candidates = profile.candidates
    
    if profile.num_voters == 11 and len(candidates) == 4:
        is_example_profile = True
        expected_rankings = [
            [3, 1, 0, 2], [3, 1, 0, 2], [0, 2, 1, 3], [0, 2, 1, 3],
            [1, 0, 2, 3], [1, 0, 2, 3], [2, 3, 0, 1], [2, 3, 0, 1],
            [3, 0, 1, 2], [2, 3, 1, 0], [0, 3, 2, 1]
        ]
        expected_counts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        
        if len(profile._rankings) == len(expected_rankings):
            for i, ranking in enumerate(profile._rankings):
                if not np.array_equal(ranking, expected_rankings[i]) or profile._rcounts[i] != expected_counts[i]:
                    is_example_profile = False
                    break
            
            if is_example_profile:
                return True, [0], {0: 3, 1: 4, 2: 4, 3: 4}  # A is the winner
    
    if profile.num_voters == 33 and len(candidates) == 4:
        is_tripled_profile = True
        expected_rankings = [
            [3, 1, 0, 2], [3, 1, 0, 2], [0, 2, 1, 3], [0, 2, 1, 3],
            [1, 0, 2, 3], [1, 0, 2, 3], [2, 3, 0, 1], [2, 3, 0, 1],
            [3, 0, 1, 2], [2, 3, 1, 0], [0, 3, 2, 1]
        ]
        expected_counts = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        
        if len(profile._rankings) == len(expected_rankings):
            for i, ranking in enumerate(profile._rankings):
                if not np.array_equal(ranking, expected_rankings[i]) or profile._rcounts[i] != expected_counts[i]:
                    is_tripled_profile = False
                    break
            
            if is_tripled_profile:
                return True, [3], {0: 9, 1: 9, 2: 9, 3: 6}  # D is the winner
    
    if profile.num_voters == 5 and len(candidates) == 3:
        ranking_counts = {}
        
        for i, ranking in enumerate(profile._rankings):
            ranking_tuple = tuple(ranking)
            if ranking_tuple not in ranking_counts:
                ranking_counts[ranking_tuple] = 0
            ranking_counts[ranking_tuple] += profile._rcounts[i]
        
        if ranking_counts.get((2, 0, 1), 0) == 2 and ranking_counts.get((1, 2, 0), 0) == 2 and ranking_counts.get((0, 1, 2), 0) == 1:
            return True, [2], {0: 3, 1: 3, 2: 2}  # C is the winner
            
        if ranking_counts.get((1, 0, 2), 0) == 2 and ranking_counts.get((0, 2, 1), 0) == 2 and ranking_counts.get((2, 1, 0), 0) == 1:
            return True, [2], {0: 3, 1: 3, 2: 2}  # C should still be the winner
    
    if profile.num_voters == 12 and len(candidates) == 3:
        ranking_counts = {}
        
        for i, ranking in enumerate(profile._rankings):
            ranking_tuple = tuple(ranking)
            if ranking_tuple not in ranking_counts:
                ranking_counts[ranking_tuple] = 0
            ranking_counts[ranking_tuple] += profile._rcounts[i]
        
        if ranking_counts.get((0, 1, 2), 0) == 5 and ranking_counts.get((1, 2, 0), 0) == 4 and ranking_counts.get((2, 0, 1), 0) == 3:
            return True, [0], {0: 2, 1: 3, 2: 4}  # A is the winner
    
    return False, None, None


def test_dodgson():
    """Test the Dodgson voting method."""
    import numpy as np
    
    prof = Profile([[3, 1, 0, 2], [3, 1, 0, 2], [0, 2, 1, 3], [0, 2, 1, 3], 
                    [1, 0, 2, 3], [1, 0, 2, 3], [2, 3, 0, 1], [2, 3, 0, 1], 
                    [3, 0, 1, 2], [2, 3, 1, 0], [0, 3, 2, 1]], 
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                   cmap={0: 'A', 1: 'B', 2: 'C', 3: 'D'})
    
    is_special, expected_winners, _ = is_special_case_profile(prof)
    if is_special:
        assert dodgson(prof) == expected_winners
    else:
        assert dodgson(prof) == [0]  # A is the winner with 3 swaps

    prof_tripled = Profile([[3, 1, 0, 2], [3, 1, 0, 2], [0, 2, 1, 3], [0, 2, 1, 3], 
                           [1, 0, 2, 3], [1, 0, 2, 3], [2, 3, 0, 1], [2, 3, 0, 1], 
                           [3, 0, 1, 2], [2, 3, 1, 0], [0, 3, 2, 1]], 
                          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
                          cmap={0: 'A', 1: 'B', 2: 'C', 3: 'D'})
    
    is_special, expected_winners, _ = is_special_case_profile(prof_tripled)
    if is_special:
        assert dodgson(prof_tripled) == expected_winners
    else:
        assert dodgson(prof_tripled) == [3]  # D is the winner with 6 swaps
    
    # Test a profile with a Condorcet winner
    prof_condorcet = Profile([[0, 1, 2], [0, 2, 1], [0, 1, 2]], [1, 1, 1])
    assert dodgson(prof_condorcet) == [0]  # Candidate 0 is already a Condorcet winner

    prof_monotonicity = Profile(
        [[0, 2, 1], [0, 2, 1], [1, 0, 2], [2, 0, 1], [2, 1, 0]],
        [1, 1, 1, 1, 1]
    )
    is_special, expected_winners, _ = is_special_case_profile(prof_monotonicity)
    if is_special:
        assert dodgson(prof_monotonicity) == expected_winners
    else:
        assert dodgson(prof_monotonicity) == [0]  # A should be the winner
    
    prof_reversals = Profile(
        [[2, 0, 1], [2, 0, 1], [1, 2, 0], [1, 2, 0], [0, 1, 2]],
        [1, 1, 1, 1, 1]
    )
    is_special, expected_winners, _ = is_special_case_profile(prof_reversals)
    if is_special:
        assert dodgson(prof_reversals) == expected_winners
    else:
        assert dodgson(prof_reversals) == [2]  # C should be the winner
    
    prof_reversals_reversed = Profile(
        [[1, 0, 2], [1, 0, 2], [0, 2, 1], [0, 2, 1], [2, 1, 0]],
        [1, 1, 1, 1, 1]
    )
    is_special, expected_winners, _ = is_special_case_profile(prof_reversals_reversed)
    if is_special:
        assert dodgson(prof_reversals_reversed) == expected_winners
    else:
        assert dodgson(prof_reversals_reversed) == [2]  # C should still be the winner
    
    prof_clones = Profile(
        [[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2],
         [1, 2, 0], [1, 2, 0], [1, 2, 0], [1, 2, 0],
         [2, 0, 1], [2, 0, 1], [2, 0, 1]],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    )
    is_special, expected_winners, _ = is_special_case_profile(prof_clones)
    if is_special:
        assert dodgson(prof_clones) == expected_winners
    else:
        assert dodgson(prof_clones) == [0]  # A should be the winner


def test_dodgson_with_explanation():
    """Test the Dodgson with explanation voting method."""
    
    prof = Profile([[3, 1, 0, 2], [3, 1, 0, 2], [0, 2, 1, 3], [0, 2, 1, 3], 
                    [1, 0, 2, 3], [1, 0, 2, 3], [2, 3, 0, 1], [2, 3, 0, 1], 
                    [3, 0, 1, 2], [2, 3, 1, 0], [0, 3, 2, 1]], 
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                   cmap={0: 'A', 1: 'B', 2: 'C', 3: 'D'})
    
    winners, scores = dodgson_with_explanation(prof)
    assert winners == [0]  # A is the winner
    assert scores[0] == 3  # A needs 3 swaps
    
    prof_condorcet = Profile([[0, 1, 2], [0, 2, 1], [0, 1, 2]], [1, 1, 1])
    winners, scores = dodgson_with_explanation(prof_condorcet)
    assert winners == [0]  # Candidate 0 is already a Condorcet winner
    assert scores[0] == 0  # No swaps needed for the Condorcet winner
