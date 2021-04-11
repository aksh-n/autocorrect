from typing import Iterator


def levenshtein_dynamic(s1: str, s2: str) -> int:
    """Returns the minimum edit distance between strings s1 and s2.
    This function implements the Levenshtein distance algorithm using Dynamic Programming.

    Note: This function is not required by the levenshtein automaton, but I felt it that
    it could be useful to illustrate the basic idea of the Levenshtein algorithm. 
    """
    dp = list(range(0, len(s2) + 1))  # dp stands for dynamic programming
    # technically, I can reduce len(dp) to min(len(s1), len(s2)), but its not necessary.

    for i in range(len(s1)):
        for d in range(len(dp) - 1, 0, -1):
            j = d - 1
            dp[d] = min(dp[d] + 1, dp[d - 1] + (s1[i] != s2[j]))
        dp[0] = i + 1
        for d in range(1, len(dp)):
            dp[d] = min(dp[d], dp[d - 1] + 1)
        # print(dp)
    return dp[-1]


def levenshtein_using_nfa(s1: str, s2: str, D: int = 2) -> int:
    """Returns the minimum edit distance between strings s1 and s2 as long as it is atmost
    D, the max edits allowed. If it is higher than D, then return -1.

    Note: This function is not going to be used in the project. It merely demonstrates the logic
    that will be used for autocorrection.
    """
    lev_nfa = LevenshteinNFA(s2, D)
    initial_states = lev_nfa.initial_states()
    final_states = lev_nfa.step_all(initial_states, s1)
    return lev_nfa.accept_best(final_states)


class NFA:
    """A Non-Finite Deterministic Automaton abstract class.
    
    Note: Some parameters and/or return value(s) of some methods are intentionally type annotated
    as the type annotation depends on how the child classes implement these methods.
    """
    def initial_states(self):
        """Returns the initial state(s)."""
        raise NotImplementedError
    
    def accept(self, state):
        """Returns whether the given state is a terminal node in the NFA."""
        raise NotImplementedError

    def transitions(self, state, c):
        """Yields a new state(s) given a state and input c."""
        raise NotImplementedError

    def step(self, states, c) -> set:
        """Returns a new set of states, which are created by transitioning from the given
        states using input c.
        """
        next_states = set()
        for state in states:
            next_states |= set(self.transitions(state, c))
        next_states = self.simplify(next_states)
        return next_states
    
    def step_all(self, states, inputs) -> set:
        """Returns the new set of states, which are created by transitioning from the given
        states using multiple inputs given in inputs.
        """
        next_states = states
        # uses a similar approach to Breadth-First Search
        for c in inputs:
            next_states = self.step(next_states, c)
        return next_states
    
    def simplify(self, states) -> set:
        """Returns an equivalent, reduced set of the given states. It is the identity function
        by default.
        """
        return states


class LevenshteinNFA(NFA):
    """A Levenshtein Non-Finite Automaton.
    
    Instance Attributes:
        - query: the query string
        - D: max D number of edits allowed (or maximum levenshtein distance D allowed)
    
    Note:
    The state parameter in the below functions is a tuple of two integers.
    The first integer, called the offset, indicates how much of the query string has been matched.
    For example, offset = 2 means that the first two letters of the query string has been matched.
    The second integer indicates the max number of edits allowed for THAT state.
    This is calculated by self.D - the number of edits used leading up to that state.
    """
    def __init__(self, query: str, D: int = 2) -> None:
        """Initializes a Levenshtein Automaton based on the query string with D max edits
        allowed.
        """
        self.query = query
        self.D = D

    def initial_states(self) -> set:
        """Returns the initial state in a set. 
        The initial state starts at offset = 0 and self.D max edits allowed.
        """
        return {(0, self.D)}
    
    def accept(self, state: tuple) -> bool:
        """Returns whether the state is a terminal node, indicating that the query string
        has been matched."""
        offset, d = state
        return len(self.query) - offset <= d
    
    def accept_best(self, states: set) -> int:
        """Returns the least number of edits used, among all terminal nodes in states.
        
        If there are no terminal nodes, then returns -1.
        """
        edits_used = float("inf")
        for state in states:
            if self.accept(state):
                edits_used = min(edits_used, self.D - state[1])
        if edits_used == float("inf"):
            return -1
        else:
            return edits_used

    def transitions(self, state: tuple, c: str) -> Iterator[tuple]:
        """Yields new state(s), given a state and the input character."""
        offset, d = state
        # when c is NOT used to match with the query string
        if d > 0:
            # deletion of c
            yield (offset, d - 1)
            # substitution of c with self.query[offset]
            yield (offset + 1, d - 1)
        # when c is used to match with the query string
        for k in range(min(d + 1, len(self.query) - offset)):
            if c == self.query[offset + k]:
                # k edits used
                yield offset + k + 1, d - k
    
    def simplify(self, states: set) -> set:
        """Returns a equivalent, reduced set of the given states."""
    
        def _implies(state1: tuple, state2: tuple) -> bool:
            """Returns whether state1 implies state2.
            More precisely, it checks whether exploring state1 also explores state2.

            The rule is that any state (n, d) for some positive integers n and d, also imply state
            (n + k, d - |k|) for some positive/negative integer k as it is just a matter of 
            inserting/deleting k times.
            """
            offset1, d1 = state1
            offset2, d2 = state2
            if d2 < 0:  # more than max edits done, so state2 is redundant regardless of state1
                return True
            return d1 - d2 >= abs(offset1 - offset2)
        
        def _is_useful(state: tuple) -> bool:
            """Returns whether the given state in the set states is useful or not.
            A state is useful if and only if there does not exist another distinct state that
            implies the state. 
            
            Preconditions:
                - state in states
            """
            for state2 in states:
                if state != state2 and _implies(state2, state):
                    return False
            return True
        
        return filter(_is_useful, states)
        
        
