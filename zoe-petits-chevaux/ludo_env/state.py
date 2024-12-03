from enum import Enum


class State_NO_EXACT_MATCH(Enum):
    ECURIE = 0
    CHEMIN = 1
    ESCALIER = 2
    OBJECTIF = 3

    @staticmethod
    def get_state_from_position(relative_position: int):
        assert 0 <= relative_position <= 63, "Position invalide"
        if relative_position == 0:
            return State_NO_EXACT_MATCH.ECURIE
        elif relative_position < 57:
            return State_NO_EXACT_MATCH.CHEMIN
        elif relative_position < 63:
            return State_NO_EXACT_MATCH.ESCALIER
        else:
            return State_NO_EXACT_MATCH.OBJECTIF


class State_EXACT_MATCH_REQUIRED(Enum):
    ECURIE = 0
    CHEMIN = 1
    PIED_ESCALIER = 2
    ESCALIER = 3
    OBJECTIF = 4

    @staticmethod
    def get_state_from_position(relative_position: int):
        assert 0 <= relative_position <= 63, "Position invalide"
        if relative_position == 0:
            return State_EXACT_MATCH_REQUIRED.ECURIE
        elif relative_position < 56:
            return State_EXACT_MATCH_REQUIRED.CHEMIN
        elif relative_position == 56:
            return State_EXACT_MATCH_REQUIRED.PIED_ESCALIER
        elif relative_position < 63:
            return State_EXACT_MATCH_REQUIRED.ESCALIER
        else:
            return State_EXACT_MATCH_REQUIRED.OBJECTIF