import numpy as np
import requests
import re
from collections import Counter

class WordleSolver:
    TARGET_PATTERN = "22222"

    def __init__(self, word_list):
        self.potential_options = word_list

    @staticmethod
    def get_pattern(target, guess):
        target_count = Counter(target)
        guess_count = Counter(guess)
        arr = np.zeros(5)

        for i in range(5):
            if target[i] == guess[i]:
                arr[i] = 2
                target_count[target[i]] -= 1
                guess_count[guess[i]] -= 1

        for i in range(5):
            if arr[i] != 2 and guess[i] in target_count and target_count[guess[i]] > 0:
                arr[i] = 1
                target_count[guess[i]] -= 1

        return arr

    def compute_entropy(self, guess):
        patterns = {}
        for target in self.potential_options:
            pattern = tuple(self.get_pattern(target, guess))
            patterns[pattern] = patterns.get(pattern, 0) + 1
        
        vals = np.array(list(patterns.values()))
        probs = vals / sum(vals)
        information = -np.log(probs)
        return np.dot(probs, information)
    
    def modify_word_list(self, guess, result):
        modified = []
        result_tuple = tuple(result)
        for word in self.potential_options:
            pattern = self.get_pattern(word, guess)
            if tuple(pattern) == result_tuple:
                modified.append(word)
        self.potential_options = modified
    
    def best_candidates(self):
        res = {}
        for guess in self.potential_options:
            score = self.compute_entropy(guess)
            if score not in res:
                res[score] = []
            res[score].append(guess)
        return res
        
    def show_5_best(self):
        scores = self.best_candidates()
        res = []
        sorted_scores = dict(sorted(scores.items(), reverse=True))
        for key in sorted_scores.keys():
            res += scores[key]
            if len(res) >= 5:
                break
        return res[:5]
    
    def solve(self):
        result = ""
        count = 0
        while True:
            guess = input("Your guess: ")
            while len(guess) != 5 or not guess.isalpha() or not guess.islower():
                print("Invalid guess. Please enter a valid 5-letter word.")
                guess = input("Your guess: ")
            result = input("Pattern you got as a result of the guess: ")
            while len(result) != 5 or not result.isdigit() or any(c not in '012' for c in result):
                print("Invalid pattern. Please enter a valid 5-digit pattern (e.g., 00210).")
                result = input("Pattern you got as a result of the guess: ")
            if result == self.TARGET_PATTERN:
                break
            arr = np.array([int(num) for num in list(result)])
            self.modify_word_list(guess, arr)
            five_best = self.show_5_best()
            print(f"The five best next guesses are: {', '.join(five_best)}")
            count += 1
        print(f"Guessed in {count} attempts")
        return
    
    # Fetch word list from the internet
def fetch_word_list():
    print('Fetching word list...')
    meaningpedia_resp = requests.get("https://meaningpedia.com/5-letter-words?show=all")
    pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
    word_list = pattern.findall(meaningpedia_resp.text)
    return word_list

# Main function to run the program
def main():
    # Fetch the word list and initialize the solver
    word_list = fetch_word_list()
    solver = WordleSolver(word_list)
    
    # Call the solver to start the game
    solver.solve()

# If the script is run directly, start the program by calling main()
if __name__ == "__main__":
    main()
