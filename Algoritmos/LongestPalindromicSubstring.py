class Solution:
    def longestPalindre(self, word: str) -> str:

        n = len(word)
        dp = [[False]*n for _ in range(n)]
        ans = [0] * 2

        # Por vacuidad
        for i in range(0,n,1):
            dp[i][i] = True
        # Palindromos de len 2
        for i in range(0,n-1,1):
            if (word[i] == word[i+1]):
                dp[i][i+1] = True
                ans = [i,i+1]
        # Por cada longitud-1 chequear cada subcadena de esa longitud y su subcadena anterior i+1 j-1
        for diff in range(2,n,1):
            for i in range(0, n-diff,1):
                j = i+diff
                if (word[i]==word[j] and dp[i+1][j-1]):
                    dp[i][j] = True
                    ans = [i,j]

        return word[ans[0]:ans[1]+1]

# abccba

#   0 1 2 3 4 5
# 0 T         T
# 1   T     T
# 2     T T 
# 3       T   
# 4         T
# 5           T