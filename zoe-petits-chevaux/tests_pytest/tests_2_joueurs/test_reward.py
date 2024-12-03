import pytest
from ludo_env import *


def test_reward():
    assert get_default_action_order(2, "not_exact") == [0, 
                                                        1, 2,
                                                        12, 7, 
                                                        11, 6,
                                                        9, 4,
                                                        10, 5,
                                                        8, 3]
    assert get_default_action_order(3, "not_exact") == [0, 
                                                        1, 2,
                                                        17, 12, 7, 
                                                        16 ,11, 6,
                                                        14 ,9, 4,
                                                        15, 10, 5,
                                                        13, 8, 3]
    assert get_default_action_order(4, "not_exact") == [0, 
                                                        1, 2,
                                                        22, 17, 12, 7, 
                                                        21, 16 ,11, 6,
                                                        19, 14 ,9, 4,
                                                        20, 15, 10, 5,
                                                        18, 13, 8, 3]

    assert get_default_action_order(2, "exact") == [0, 
                                                        1, 2,
                                                        14, 8, 
                                                        13, 7, 
                                                        10, 4, 
                                                        11, 5,
                                                        12, 6,
                                                        9, 3]
    assert get_default_action_order(3, "exact") == [0, 
                                                        1, 2,
                                                        20, 14, 8, 
                                                        19, 13, 7, 
                                                        16, 10, 4, 
                                                        17, 11, 5,
                                                        18, 12, 6,
                                                       15,  9, 3]
    assert get_default_action_order(4, "exact") == [0, 
                                                        1, 2,
                                                        26, 20, 14, 8, 
                                                        25,19, 13, 7, 
                                                        22, 16, 10, 4, 
                                                        23,17, 11, 5,
                                                        24,18, 12, 6,
                                                       21, 15,  9, 3]                                                

