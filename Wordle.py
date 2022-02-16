from enum import Enum
import random
import re


class Marker(Enum):
    GREEN=0
    YELLOW=1
    GRAY=2


class GameMaster:
    
    def __init__(self, answer, candidates, quiet=False):
        self.answer = answer
        self.counter = 0
        self.game_win = False
        self.word_size = 5
        self.guesses= []
        self.hints = []
        self.word_candidates = candidates
        self.quiet = quiet
                
    def is_game_win(self, hint):
        game_win = all([int(h) == Marker.GREEN.value for h in hint])
        self.game_win = game_win
        if self.game_win and not self.quiet:
            print("=== Win ===")
        return self.game_win

    def _is_valid_input(self, input):
        if len(input) != self.word_size:
            return False
        if input not in self.word_candidates:
            return False
        return True

    def check(self, word):
        if not self._is_valid_input(word):
            raise ValueError
        
        hint = []
        for i, p in enumerate(word):
            if p == self.answer[i]:
                marker = Marker.GREEN.value
            elif p in self.answer:
                marker = Marker.YELLOW.value
            else:
                marker = Marker.GRAY.value
            hint.append(marker)
        hint = "".join(map(str, hint))
        
        self.guesses.append(word)
        self.hints.append(hint)
        self.counter += 1
        
        self.is_game_win(hint)

        return hint


class WordleUtil:
    
    @staticmethod
    def search(words, pattern):
        candidates = []
        for w in words:
            if re.match(pattern, w):
                candidates.append(w)
        return candidates
    
    @staticmethod
    def hint2pattern(word, hint):
        pattern = ["^"]
        
        greens = "".join([word[i] if int(h) == Marker.GREEN.value else "." for i, h in enumerate(hint)])
        pattern.append(f"(?={greens})")

        pos_yellows = "".join([ f"(?=.*{word[i]})"  for i, h in enumerate(hint) if int(h) == Marker.YELLOW.value])
        pattern.append(pos_yellows)
        
        neg_yellows = []
        for i, h in enumerate(hint):
            if int(h) == Marker.YELLOW.value:
                _p = ["."] * len(word)
                _p[i] = word[i]
                _p = "".join(_p)
                neg_yellows.append(f"(?!{_p})")
        pattern.append("".join(neg_yellows))
        
        grays = "".join([ f"(?!.*{word[i]})"  for i, h in enumerate(hint) if int(h) == Marker.GRAY.value])
        pattern.append(grays)
        
        pattern.append("[a-z]{5}$")
        return "".join(pattern)
    

class SimpleSolver:
    
    def __init__(self, words):
        self.candidates = words    
            
    def guess(self, word: str, hint: str):
        """Simple Solver

        Args:
            word (str): hintに対応する単語
            hint (str): ゲームで得られるヒント. ex. "01123"

        Returns:
            [str]: 推測した単語
        """
        if word is not None and hint is not None:
            pattern = WordleUtil.hint2pattern(word, hint)
            self.candidates = WordleUtil.search(self.candidates, pattern)
        return random.choice(self.candidates)
