import pytest
from ludo_env import GameLogic, Action_EXACT_MATCH_REQUIRED


@pytest.fixture
def game_2chevaux_exact_match():
    return  GameLogic(num_players=2, nb_chevaux=2, mode_pied_escalier="exact_match")


def test_valid_actions_exact_match(game_2chevaux_exact_match):
    game_2chevaux_exact_match.board[0] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact_match.get_valid_actions(0, 1) == [ [], [Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER] ,False] 
    assert game_2chevaux_exact_match.get_valid_actions(0, 2) == [ [], [] ,Action_EXACT_MATCH_REQUIRED.NO_ACTION]  
    assert game_2chevaux_exact_match.get_valid_actions(0, 3) == [ [], [] , Action_EXACT_MATCH_REQUIRED.NO_ACTION]  
    assert game_2chevaux_exact_match.get_valid_actions(0, 4) == [ [], [] , Action_EXACT_MATCH_REQUIRED.NO_ACTION] 
    assert game_2chevaux_exact_match.get_valid_actions(0, 5) == [ [], [] , Action_EXACT_MATCH_REQUIRED.NO_ACTION]  
    assert game_2chevaux_exact_match.get_valid_actions(0, 6) == [ [Action_EXACT_MATCH_REQUIRED.MOVE_OUT], [] ,False]  

    game_2chevaux_exact_match.board[0] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact_match.get_valid_actions(0, 1) == [ [], [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD] ,False]  
    assert game_2chevaux_exact_match.get_valid_actions(0, 2) == [ [], [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD] ,False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 3) == [ [], [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD] ,False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 4) == [ [], [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD] ,False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 5) == [ [], [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD] ,False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 6) ==  [ [Action_EXACT_MATCH_REQUIRED.MOVE_OUT], [Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER] ,False]   

    # bloquer un pion adverse sur case 56
    game_2chevaux_exact_match.board[0] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    game_2chevaux_exact_match.board[1] = [ 1, 
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact_match.get_valid_actions(0, 1) ==   [ [], [Action_EXACT_MATCH_REQUIRED.KILL ] ,False]  
    assert game_2chevaux_exact_match.get_valid_actions(0, 2) == [ [], [], Action_EXACT_MATCH_REQUIRED.NO_ACTION]    
    assert game_2chevaux_exact_match.get_valid_actions(0, 3) == [ [], [], Action_EXACT_MATCH_REQUIRED.NO_ACTION]     
    assert game_2chevaux_exact_match.get_valid_actions(0, 4) == [ [], [], Action_EXACT_MATCH_REQUIRED.NO_ACTION]     
    assert game_2chevaux_exact_match.get_valid_actions(0, 5) == [ [], [], Action_EXACT_MATCH_REQUIRED.NO_ACTION]     
    assert game_2chevaux_exact_match.get_valid_actions(0, 6) == [ [Action_EXACT_MATCH_REQUIRED.MOVE_OUT], [], False]     

    # bloquer un pion adverse sur case avant 56 
    game_2chevaux_exact_match.board[0] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    game_2chevaux_exact_match.board[1] = [ 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact_match.get_valid_actions(0, 1) == [ [], [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 2) == [ [], [Action_EXACT_MATCH_REQUIRED.KILL], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 3) == [ [], [Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER], False]    
    assert game_2chevaux_exact_match.get_valid_actions(0, 4) == [ [], [Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 5) == [ [], [Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 6) == [ [Action_EXACT_MATCH_REQUIRED.MOVE_OUT_AND_KILL], [], False]   

    # se bloquer un pion avant case 56 
    game_2chevaux_exact_match.board[0] = [ 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    game_2chevaux_exact_match.board[1] = [ 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact_match.get_valid_actions(0, 1) == [ [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 2) == [ [], [Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 3) == [ [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], [Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 4) == [ [Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER], [], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 5) == [ [Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER], [], False]   
    assert game_2chevaux_exact_match.get_valid_actions(0, 6) == [ [Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER], [],False]   

def test_exact_match_escalier(game_2chevaux_exact_match):
    pass 
    # TODO 


@pytest.fixture
def game_3chevaux_exact_match():
    return GameLogic(num_players=2, nb_chevaux=3, mode_pied_escalier="exact_match")


@pytest.fixture
def game_4chevaux_exact_match():
    return GameLogic(num_players=2, nb_chevaux=4, mode_pied_escalier="exact_match")




# def test_get_valid_actions(game_4chevaux_exact_match):
#     game_4chevaux_exact_match.board[0] = [ 0,
#                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 
#                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
#                 0, 0, 0, 0, 0, 0,
#                 0]
#     print(game_4chevaux_exact_match.get_valid_actions(0, 1))
#     assert game_4chevaux_exact_match.get_valid_actions(0, 1) == [[Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact_match.get_valid_actions(0, 2) == [[Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact_match.get_valid_actions(0, 3) == [[Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact_match.get_valid_actions(0, 4) == [[Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact_match.get_valid_actions(0, 5) == [[Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact_match.get_valid_actions(0, 6) == [[Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
    
    
