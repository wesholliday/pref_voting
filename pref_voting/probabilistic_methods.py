'''
    File: voting_methods.py
    Author: Wes Holliday (wesholliday@berkeley.edu) and Eric Pacuit (epacuit@umd.edu)
    Date: June 3, 2023
    
    Implementations of probabilistic voting methods.
'''

from pref_voting.prob_voting_method import  *
from pref_voting.weighted_majority_graphs import  MajorityGraph, MarginGraph
import random
import nashpy as nash

@pvm(name="Random Dictator")
def random_dictator(profile, curr_cands = None): 
    '''Returns lottery over the candidates that is proportional to the Plurality scores. 

    Args:
        profile (Profile): A Profile object.
        curr_cands (list): A list of candidates to restrict the ranking to. If ``None``, then the ranking is over the entire domain of the profile.

    Returns:
        dict: A dictionary mapping candidates to probabilities.
    ''' 
    
    plurality_scores = profile.plurality_scores(curr_cands = curr_cands)
    total_plurality_scores = sum(list(plurality_scores.values()))

    return {c: plurality_scores[c] / total_plurality_scores for c in plurality_scores.keys()}

@pvm(name="Proportional Borda")
def pr_borda(profile, curr_cands=None): 
    '''Returns lottery over the candidates that is proportional to the Borda scores.
    
    Args:   
        profile (Profile): A Profile object.
        curr_cands (list): A list of candidates to restrict the ranking to. If ``None``, then the ranking is over the entire domain of the profile.

    Returns:
        dict: A dictionary mapping candidates to probabilities.
    
    '''
    borda_scores = profile.borda_scores(curr_cands=curr_cands)
    total_borda_scores = sum(list(borda_scores.values()))

    return {c: borda_scores[c] / total_borda_scores for c in borda_scores.keys()}


def _maximal_lottery(edata, curr_cands = None, margin_transformation = lambda x: x):
    '''Implementation of maximal lotteries.   See http://dss.in.tum.de/files/brandt-research/fishburn_slides.pdf 
    
    Returns a randomly chosen maximal lottery.
    '''

    candidates = edata.candidates if curr_cands is None else curr_cands
    m_matrix, cand_to_cidx = edata.strength_matrix(curr_cands=candidates)

    A = np.array([[margin_transformation(m) for m in row] 
                  for row in m_matrix])

    # Create the game
    game = nash.Game(A)
    # Find the Nash Equilibrium with Vertex Enumeration
    equilibria = list(game.vertex_enumeration())
    if len(equilibria) == 0:
        return {c: 1/len(candidates) for c in candidates}
    else:
        eq = random.choice(equilibria)
        return {c: eq[0][cand_to_cidx(c)] for c in candidates}

@pvm(name="C1 Maximal Lottery")
def c1_maximal_lottery(edata, curr_cands=None): 

    '''Returns the C1 maximal lottery over the candidates.  See http://dss.in.tum.de/files/brandt-research/fishburn_slides.pdf.
    
    Args:   
        edata (Profile, MarginGraph): A Profile object.
        curr_cands (list): A list of candidates to restrict the ranking to. If ``None``, then the ranking is over the entire domain of the profile.
    
    Returns:
        dict: A dictionary mapping candidates to probabilities.
    '''

    if type(edata) == MajorityGraph:
        # if edata is a MajorityGraph, we need to add margins for the following code to work.  The margins do not matter when finding the c1 maximal lottery.

        candidates = edata.candidates if curr_cands is None else curr_cands 
          
        edata = MarginGraph(candidates, [(c1, c2, 1) for c1, c2 in edata.edges if (c1 in candidates and c2 in candidates)])

    return _maximal_lottery(edata, 
                            curr_cands=curr_cands, 
                            margin_transformation = np.sign)

@pvm(name="Maximal Lottery")
def maximal_lottery(edata, curr_cands=None): 
    '''Returns the maximal lottery over the candidates.  See http://dss.in.tum.de/files/brandt-research/fishburn_slides.pdf.
    
    Args:   
        edata (Profile, MarginGraph): A Profile object.
        curr_cands (list): A list of candidates to restrict the ranking to. If ``None``, then the ranking is over the entire domain of the profile.


    Returns:
        dict: A dictionary mapping candidates to probabilities.
    
    '''
    return _maximal_lottery(edata, 
                            curr_cands=curr_cands, 
                            margin_transformation = lambda x: x)


@pvm(name="Random Consensus Builder")
def random_consensus_builder(profile, curr_cands=None, beta=0.6):
    """β-Random Consensus Builder (RCB) voting method.

    Args:
        profile (Profile): An anonymous profile of linear orders
        curr_cands (List[int], optional): Candidates to consider. Defaults to all candidates if not provided.
        beta (float): Threshold for elimination (default: 0.6)

    Returns:
        dict: Maps each candidate to their probability (1.0 for winner, 0.0 for others)
    """
    if curr_cands is None:
        curr_cands = profile.candidates
    elif len(curr_cands) == 0:
        return {}

    # Get all rankings and choose a random voter
    rankings = profile.rankings
    if not rankings:  # Handle empty profile case
        return {c: 1.0/len(curr_cands) for c in curr_cands}

    v = random.randrange(len(rankings))
    voter_ranking = rankings[v]

    # Track eliminated candidates
    eliminated = set()
    last_processed = None

    # Process candidates in voter's preference order (worst to best)
    for i in reversed(voter_ranking):
        if i not in curr_cands or i in eliminated:
            continue

        # Check each candidate j that v prefers over i
        for j in voter_ranking:
            if j == i or j not in curr_cands or j in eliminated:
                continue
            if voter_ranking.index(j) < voter_ranking.index(i):
                # Calculate s_{i ⪰ j}
                support_ratio = profile.support(i, j) / profile.num_voters
                if support_ratio >= beta:
                    eliminated.add(j)

        last_processed = i

    # If no candidate was processed (all eliminated), distribute probability equally
    if last_processed is None:
        return {c: 1.0/len(curr_cands) for c in curr_cands}

    # Return probability distribution (1.0 for winner, 0.0 for others)
    return {c: 1.0 if c == last_processed else 0.0 for c in curr_cands}


def create_probabilistic_method(vm):
    """
    Create a probabilistic voting method from a voting method.
    """

    from pref_voting.voting_method import VotingMethod
    if type(vm) != VotingMethod:
        raise TypeError("vm must be a VotingMethod object")

    def _pvm(profile, curr_cands=None, **kwargs):
        return vm.prob(profile, curr_cands=curr_cands, **kwargs)

    return ProbVotingMethod(_pvm, name=f'{vm.name} with Even Chance Tiebreaking')
