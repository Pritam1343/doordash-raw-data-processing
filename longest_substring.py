def length_of_longest_substring(s: str) -> int:
    char_set = set()
    for str in s:
        if str in char_set:
            return len(char_set)
        char_set.add(str)
    
    return len(char_set)

# Example usage
if __name__ == "__main__":
    s = "abcabcbb"
    print(length_of_longest_substring(s))  # Output: 3 (substring "abc")
    s = "bbbbb"
    print(length_of_longest_substring(s))  # Output: 1 (substring "b")      
    s = "pwwkew"
    print(length_of_longest_substring(s))  # Output: 3 (substring "wke")
    s = ""
    print(length_of_longest_substring(s))  # Output: 0 (empty string)