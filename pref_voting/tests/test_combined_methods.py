from pref_voting.combined_methods import *
from pref_voting.profiles import Profile
import pytest

@pytest.mark.parametrize("voting_method, expected", [
    (daunou, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (blacks, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (smith_irv, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (smith_irv_put, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (condorcet_irv, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (condorcet_irv_put, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (condorcet_plurality, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (smith_minimax, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (copeland_local_borda, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (copeland_global_borda, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    }),
    (borda_minimax_faceoff, {
        'condorcet_cycle': [0, 1, 2], 
        'linear_profile_0': [0], 
        'linear_profile_0_curr_cands': [1],
        'profile_single_voter': [0]
    })
])
def test_combined_methods(
    voting_method, expected, 
    condorcet_cycle, 
    linear_profile_0,
    profile_single_voter):
    assert voting_method(condorcet_cycle) == expected['condorcet_cycle']
    assert voting_method(linear_profile_0) == expected['linear_profile_0']
    if 'linear_profile_0_curr_cands' in expected:
        assert voting_method(linear_profile_0, curr_cands=[1, 2]) == expected['linear_profile_0_curr_cands']
    assert voting_method(profile_single_voter) == expected['profile_single_voter']


def test_compose(condorcet_cycle):
    vm = compose(plurality, borda)
    assert type(vm) == VotingMethod
    assert vm.name == "Plurality-Borda"
    assert vm(condorcet_cycle) == [0, 1, 2]

def test_faceoff(condorcet_cycle):
    vm = faceoff(plurality, borda)
    assert type(vm) == VotingMethod
    assert vm.name == "Plurality-Borda Faceoff"
    assert vm(condorcet_cycle) == [0, 1, 2]
