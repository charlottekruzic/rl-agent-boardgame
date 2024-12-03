import pytest
from ludo_env import GameLogic, Action_NO_EXACT_MATCH, Action_EXACT_MATCH_REQUIRED


@pytest.fixture
def game_2chevaux():
    return GameLogic(num_players=2, nb_chevaux=2)


@pytest.fixture
def game_3chevaux():
    return GameLogic(num_players=2, nb_chevaux=3)


@pytest.fixture
def game_4chevaux():
    return GameLogic(num_players=2, nb_chevaux=4)



def test_decode_2chevaux(game_2chevaux):
    assert game_2chevaux.decode_action(0) == (0, Action_NO_EXACT_MATCH.NO_ACTION)
    assert game_2chevaux.decode_action(1) == (0, Action_NO_EXACT_MATCH.MOVE_OUT)
    assert game_2chevaux.decode_action(2) == (0, Action_NO_EXACT_MATCH.MOVE_OUT_AND_KILL)

    assert game_2chevaux.decode_action(3) == (0, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_2chevaux.decode_action(4) == (0, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_2chevaux.decode_action(5) == (0, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_2chevaux.decode_action(6) == (0, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_2chevaux.decode_action(7) == (0, Action_NO_EXACT_MATCH.KILL)

    assert game_2chevaux.decode_action(8) == (1, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_2chevaux.decode_action(9) == (1, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_2chevaux.decode_action(10) == (1, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_2chevaux.decode_action(11) == (1, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_2chevaux.decode_action(12) == (1, Action_NO_EXACT_MATCH.KILL)


def test_decode_3chevaux(game_3chevaux):
    assert game_3chevaux.decode_action(0) == (0, Action_NO_EXACT_MATCH.NO_ACTION)
    assert game_3chevaux.decode_action(1) == (0, Action_NO_EXACT_MATCH.MOVE_OUT)
    assert game_3chevaux.decode_action(2) == (0, Action_NO_EXACT_MATCH.MOVE_OUT_AND_KILL)

    assert game_3chevaux.decode_action(3) == (0, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_3chevaux.decode_action(4) == (0, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_3chevaux.decode_action(5) == (0, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux.decode_action(6) == (0, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_3chevaux.decode_action(7) == (0, Action_NO_EXACT_MATCH.KILL)

    assert game_3chevaux.decode_action(8) == (1, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_3chevaux.decode_action(9) == (1, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_3chevaux.decode_action(10) == (1, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux.decode_action(11) == (1, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_3chevaux.decode_action(12) == (1, Action_NO_EXACT_MATCH.KILL)

    assert game_3chevaux.decode_action(13) == (2, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_3chevaux.decode_action(14) == (2, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_3chevaux.decode_action(15) == (2, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux.decode_action(16) == (2, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_3chevaux.decode_action(17) == (2, Action_NO_EXACT_MATCH.KILL)

def test_decode_4chevaux(game_4chevaux):
    assert game_4chevaux.decode_action(0) == (0, Action_NO_EXACT_MATCH.NO_ACTION)
    assert game_4chevaux.decode_action(1) == (0, Action_NO_EXACT_MATCH.MOVE_OUT)
    assert game_4chevaux.decode_action(2) == (0, Action_NO_EXACT_MATCH.MOVE_OUT_AND_KILL)

    assert game_4chevaux.decode_action(3) == (0, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_4chevaux.decode_action(4) == (0, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_4chevaux.decode_action(5) == (0, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.decode_action(6) == (0, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_4chevaux.decode_action(7) == (0, Action_NO_EXACT_MATCH.KILL)

    assert game_4chevaux.decode_action(8) == (1, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_4chevaux.decode_action(9) == (1, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_4chevaux.decode_action(10) == (1, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.decode_action(11) == (1, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_4chevaux.decode_action(12) == (1, Action_NO_EXACT_MATCH.KILL)

    assert game_4chevaux.decode_action(13) == (2, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_4chevaux.decode_action(14) == (2, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_4chevaux.decode_action(15) == (2, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.decode_action(16) == (2, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_4chevaux.decode_action(17) == (2, Action_NO_EXACT_MATCH.KILL)

    assert game_4chevaux.decode_action(18) == (3, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert game_4chevaux.decode_action(19) == (3, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert game_4chevaux.decode_action(20) == (3, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.decode_action(21) == (3, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert game_4chevaux.decode_action(22) == (3, Action_NO_EXACT_MATCH.KILL)


def test_encode_2chevaux(game_2chevaux):
    assert 0 == game_2chevaux.encode_action(0, Action_NO_EXACT_MATCH.NO_ACTION)
    assert 1 == game_2chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_OUT)
    assert 2 == game_2chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_OUT_AND_KILL)
    assert 3 == game_2chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 4 == game_2chevaux.encode_action(0, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 5 == game_2chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 6 == game_2chevaux.encode_action(0, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 7 == game_2chevaux.encode_action(0, Action_NO_EXACT_MATCH.KILL)
    assert 8 == game_2chevaux.encode_action(1, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 9 == game_2chevaux.encode_action(1, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 10 == game_2chevaux.encode_action(1, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 11 == game_2chevaux.encode_action(1, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 12 == game_2chevaux.encode_action(1, Action_NO_EXACT_MATCH.KILL)

def test_encode_3chevaux(game_3chevaux):
    assert 0 == game_3chevaux.encode_action(0, Action_NO_EXACT_MATCH.NO_ACTION)
    assert 1 == game_3chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_OUT)
    assert 2 == game_3chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_OUT_AND_KILL)
    assert 3 == game_3chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 4 == game_3chevaux.encode_action(0, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 5 == game_3chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 6 == game_3chevaux.encode_action(0, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 7 == game_3chevaux.encode_action(0, Action_NO_EXACT_MATCH.KILL)
    assert 8 == game_3chevaux.encode_action(1, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 9 == game_3chevaux.encode_action(1, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 10 == game_3chevaux.encode_action(1, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 11 == game_3chevaux.encode_action(1, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 12 == game_3chevaux.encode_action(1, Action_NO_EXACT_MATCH.KILL)
    assert 13 == game_3chevaux.encode_action(2, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 14 == game_3chevaux.encode_action(2, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 15 == game_3chevaux.encode_action(2, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 16 == game_3chevaux.encode_action(2, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 17 == game_3chevaux.encode_action(2, Action_NO_EXACT_MATCH.KILL)

def test_encode_4chevaux(game_4chevaux):
    assert 0 == game_4chevaux.encode_action(0, Action_NO_EXACT_MATCH.NO_ACTION)
    assert 1 == game_4chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_OUT)
    assert 2 == game_4chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_OUT_AND_KILL)
    assert 3 == game_4chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 4 == game_4chevaux.encode_action(0, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 5 == game_4chevaux.encode_action(0, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 6 == game_4chevaux.encode_action(0, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 7 == game_4chevaux.encode_action(0, Action_NO_EXACT_MATCH.KILL)
    assert 8 == game_4chevaux.encode_action(1, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 9 == game_4chevaux.encode_action(1, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 10 == game_4chevaux.encode_action(1, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 11 == game_4chevaux.encode_action(1, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 12 == game_4chevaux.encode_action(1, Action_NO_EXACT_MATCH.KILL)
    assert 13 == game_4chevaux.encode_action(2, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 14 == game_4chevaux.encode_action(2, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 15 == game_4chevaux.encode_action(2, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 16 == game_4chevaux.encode_action(2, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 17 == game_4chevaux.encode_action(2, Action_NO_EXACT_MATCH.KILL)
    assert 18 == game_4chevaux.encode_action(3, Action_NO_EXACT_MATCH.MOVE_FORWARD)
    assert 19 == game_4chevaux.encode_action(3, Action_NO_EXACT_MATCH.ENTER_SAFEZONE)
    assert 20 == game_4chevaux.encode_action(3, Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE)
    assert 21 == game_4chevaux.encode_action(3, Action_NO_EXACT_MATCH.REACH_GOAL)
    assert 22 == game_4chevaux.encode_action(3, Action_NO_EXACT_MATCH.KILL)








@pytest.fixture
def game_2chevaux_exact_match():
    return GameLogic(num_players=2, nb_chevaux=2, mode_pied_escalier="exact_match")


@pytest.fixture
def game_3chevaux_exact_match():
    return GameLogic(num_players=2, nb_chevaux=3, mode_pied_escalier="exact_match")


@pytest.fixture
def game_4chevaux_exact_match():
    return GameLogic(num_players=2, nb_chevaux=4, mode_pied_escalier="exact_match")




def test_decode_2chevaux_exact_match(game_2chevaux_exact_match):
    assert game_2chevaux_exact_match.decode_action(0) == (0, Action_EXACT_MATCH_REQUIRED.NO_ACTION)
    assert game_2chevaux_exact_match.decode_action(1) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT)
    assert game_2chevaux_exact_match.decode_action(2) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT_AND_KILL)

    assert game_2chevaux_exact_match.decode_action(3) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert game_2chevaux_exact_match.decode_action(4) == (0, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_2chevaux_exact_match.decode_action(5) == (0, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_2chevaux_exact_match.decode_action(6) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_2chevaux_exact_match.decode_action(7) == (0, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_2chevaux_exact_match.decode_action(8) == (0, Action_EXACT_MATCH_REQUIRED.KILL)

    assert game_2chevaux_exact_match.decode_action(9) == (1, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert game_2chevaux_exact_match.decode_action(10) == (1, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_2chevaux_exact_match.decode_action(11) == (1, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_2chevaux_exact_match.decode_action(12) == (1, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_2chevaux_exact_match.decode_action(13) == (1, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_2chevaux_exact_match.decode_action(14) == (1, Action_EXACT_MATCH_REQUIRED.KILL)


def test_decode_3chevaux_exact_match(game_3chevaux_exact_match):
    assert game_3chevaux_exact_match.decode_action(0) == (0, Action_EXACT_MATCH_REQUIRED.NO_ACTION)
    assert game_3chevaux_exact_match.decode_action(1) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT)
    assert game_3chevaux_exact_match.decode_action(2) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT_AND_KILL)

    assert game_3chevaux_exact_match.decode_action(3) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)

    assert game_3chevaux_exact_match.decode_action(4) == (0, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_3chevaux_exact_match.decode_action(5) == (0, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_3chevaux_exact_match.decode_action(6) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux_exact_match.decode_action(7) == (0, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_3chevaux_exact_match.decode_action(8) == (0, Action_EXACT_MATCH_REQUIRED.KILL)

    assert game_3chevaux_exact_match.decode_action(9) == (1, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert game_3chevaux_exact_match.decode_action(10) == (1, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_3chevaux_exact_match.decode_action(11) == (1, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_3chevaux_exact_match.decode_action(12) == (1, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux_exact_match.decode_action(13) == (1, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_3chevaux_exact_match.decode_action(14) == (1, Action_EXACT_MATCH_REQUIRED.KILL)

    assert game_3chevaux_exact_match.decode_action(15) == (2, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert game_3chevaux_exact_match.decode_action(16) == (2, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_3chevaux_exact_match.decode_action(17) == (2, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_3chevaux_exact_match.decode_action(18) == (2, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux_exact_match.decode_action(19) == (2, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_3chevaux_exact_match.decode_action(20) == (2, Action_EXACT_MATCH_REQUIRED.KILL)

def test_decode_4chevaux_exact_match(game_4chevaux_exact_match):
    assert game_4chevaux_exact_match.decode_action(0) == (0, Action_EXACT_MATCH_REQUIRED.NO_ACTION)
    assert game_4chevaux_exact_match.decode_action(1) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT)
    assert game_4chevaux_exact_match.decode_action(2) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT_AND_KILL)

    assert game_4chevaux_exact_match.decode_action(3) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert game_4chevaux_exact_match.decode_action(4) == (0, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_4chevaux_exact_match.decode_action(5) == (0, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_4chevaux_exact_match.decode_action(6) == (0, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux_exact_match.decode_action(7) == (0, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_4chevaux_exact_match.decode_action(8) == (0, Action_EXACT_MATCH_REQUIRED.KILL)

    assert game_4chevaux_exact_match.decode_action(9) == (1, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert game_4chevaux_exact_match.decode_action(10) == (1, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_4chevaux_exact_match.decode_action(11) == (1, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_4chevaux_exact_match.decode_action(12) == (1, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux_exact_match.decode_action(13) == (1, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_4chevaux_exact_match.decode_action(14) == (1, Action_EXACT_MATCH_REQUIRED.KILL)

    assert game_4chevaux_exact_match.decode_action(15) == (2, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert game_4chevaux_exact_match.decode_action(16) == (2, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_4chevaux_exact_match.decode_action(17) == (2, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_4chevaux_exact_match.decode_action(18) == (2, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux_exact_match.decode_action(19) == (2, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_4chevaux_exact_match.decode_action(20) == (2, Action_EXACT_MATCH_REQUIRED.KILL)

    assert game_4chevaux_exact_match.decode_action(21) == (3, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert game_4chevaux_exact_match.decode_action(22) == (3, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert game_4chevaux_exact_match.decode_action(23) == (3, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert game_4chevaux_exact_match.decode_action(24) == (3, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux_exact_match.decode_action(25) == (3, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert game_4chevaux_exact_match.decode_action(26) == (3, Action_EXACT_MATCH_REQUIRED.KILL)


def test_encode_2chevaux_exact_match(game_2chevaux_exact_match):
    assert 0 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.NO_ACTION)
    assert 1 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT)
    assert 2 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT_AND_KILL)
    assert 3 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 4 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 5 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 6 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 7 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 8 == game_2chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.KILL)
    assert 9 == game_2chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 10 == game_2chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 11 == game_2chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 12 == game_2chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 13 == game_2chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 14 == game_2chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.KILL)

def test_encode_3chevaux_exact_match(game_3chevaux_exact_match):
    assert 0 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.NO_ACTION)
    assert 1 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT)
    assert 2 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT_AND_KILL)
    assert 3 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 4 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 5 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 6 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 7 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 8 == game_3chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.KILL)
    assert 9 == game_3chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 10 == game_3chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 11 == game_3chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 12 == game_3chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 13 == game_3chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 14 == game_3chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.KILL)
    assert 15 == game_3chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 16 == game_3chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 17 == game_3chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 18 == game_3chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 19 == game_3chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 20 == game_3chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.KILL)

def test_encode_4chevaux_exact_match(game_4chevaux_exact_match):
    assert 0 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.NO_ACTION)
    assert 1 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT)
    assert 2 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_OUT_AND_KILL)
    assert 3 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 4 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 5 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 6 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 7 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 8 == game_4chevaux_exact_match.encode_action(0, Action_EXACT_MATCH_REQUIRED.KILL)
    assert 9 == game_4chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 10 == game_4chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 11 == game_4chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 12 == game_4chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 13 == game_4chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 14 == game_4chevaux_exact_match.encode_action(1, Action_EXACT_MATCH_REQUIRED.KILL)
    assert 15 == game_4chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 16 == game_4chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 17 == game_4chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 18 == game_4chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 19 == game_4chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 20 == game_4chevaux_exact_match.encode_action(2, Action_EXACT_MATCH_REQUIRED.KILL)
    assert 21 == game_4chevaux_exact_match.encode_action(3, Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD)
    assert 22 == game_4chevaux_exact_match.encode_action(3, Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER)
    assert 23 == game_4chevaux_exact_match.encode_action(3, Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER)
    assert 24 == game_4chevaux_exact_match.encode_action(3, Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE)
    assert 25 == game_4chevaux_exact_match.encode_action(3, Action_EXACT_MATCH_REQUIRED.REACH_GOAL)
    assert 26 == game_4chevaux_exact_match.encode_action(3, Action_EXACT_MATCH_REQUIRED.KILL)