"""A (temporary file) that includes the levenshtein distance function."""

def levenshtein(s1: str, s2: str) -> int:
    """Returns the minimum edit distance between strings s1 and s2.
    This function implements the Levenshtein distance algorithm using Dynamic Programming.
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
        print(dp)
    return dp[-1]