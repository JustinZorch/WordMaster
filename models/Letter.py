from typing import Dict


class Letter:

    """"
        Creates the letter class for the users
    """

    def __init__(self, pos, letter: str):

        self.pos = pos
        self.letter = letter
        self._class = "letter"
        self.bool = False

    def json(self) -> Dict:
        return {
            "pos": self.pos,
            "letter": self.letter,
            "class": self._class,
            "bool": self.bool
        }