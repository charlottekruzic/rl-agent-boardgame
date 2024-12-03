from ludo_env.action import Action_NO_EXACT_MATCH, Action_EXACT_MATCH_REQUIRED

REWARD_TABLE_MOVE_OUT = {
    Action_NO_EXACT_MATCH.NO_ACTION: -1,
    Action_NO_EXACT_MATCH.MOVE_OUT: 20,
    Action_NO_EXACT_MATCH.MOVE_OUT_AND_KILL: 10,
    Action_NO_EXACT_MATCH.MOVE_FORWARD: 5,
    Action_NO_EXACT_MATCH.ENTER_SAFEZONE: 15,
    Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT_MATCH.REACH_GOAL: 10,
    Action_NO_EXACT_MATCH.KILL: 30,
    # Action.PROTECT: 20,
    #
    # Action.DIE: -20 # TODO -> reward pas d'action enfaite, on le subit pendant un tour
}  # faudrait que les sommes répartis soient égales

REWARD_TABLE_MOVE_OUT_EXACT_MATCH = {
    Action_EXACT_MATCH_REQUIRED.NO_ACTION: -1,
    Action_EXACT_MATCH_REQUIRED.MOVE_OUT: 20,
    Action_EXACT_MATCH_REQUIRED.MOVE_OUT_AND_KILL: 10,

    Action_EXACT_MATCH_REQUIRED.MOVE_FORWARD: 5,
    Action_EXACT_MATCH_REQUIRED.REACH_PIED_ESCALIER: 15,
    Action_EXACT_MATCH_REQUIRED.AVANCE_RECULE_PIED_ESCALIER: 1,
    Action_EXACT_MATCH_REQUIRED.MOVE_IN_SAFE_ZONE: 1,

    Action_EXACT_MATCH_REQUIRED.REACH_GOAL: 10,
    Action_EXACT_MATCH_REQUIRED.KILL: 30,
}


DEFAULT_ACTION_ORDER = {
    0,  # ça veut dire rien de possible
    1,  # d'abord essayer de sortir
    6,
    11,  # tuer un pion
    3,
    8,  # sauver le pion
    5,
    10,  # atteindre l'objectif
    2,
    7,  # avancer
    4,
    9,  # avancer dans la safezone
}


## WIP : TODO les différents agents 
'''
agent 0 : random
agent 1 : maximise le nombre de chevaux sortis
agent 2 : maximise l'avancé de ses pions déjà sortis
agent 3 : aime tuer les pions des autres
agent 4 : aime mettre en sécurité ses pions
agent 5 : aime bouger le moins possible
agent 6 : aime protéger ses pions # TODO : à implémenter quand on aura les actions protect
'''

# TODO : là c'est des tables pour 2 joueurs / 2 chevaux
# faire en sorte d'avoir des fonctions pour nb joueurs / nb chevaux

AGENT_0_REWARD_TABLE = {
    Action_NO_EXACT_MATCH.NO_ACTION: -1,
    Action_NO_EXACT_MATCH.MOVE_OUT: 1,
    Action_NO_EXACT_MATCH.MOVE_FORWARD: 1,
    Action_NO_EXACT_MATCH.ENTER_SAFEZONE: 1,
    Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT_MATCH.REACH_GOAL: 1,
    Action_NO_EXACT_MATCH.KILL: 1,
}

# TODO : si agent 0 : faire un random pour order

AGENT_1_REWARD_TABLE = {
    Action_NO_EXACT_MATCH.NO_ACTION: -1,
    Action_NO_EXACT_MATCH.MOVE_OUT: 10,
    Action_NO_EXACT_MATCH.MOVE_FORWARD: 1,
    Action_NO_EXACT_MATCH.ENTER_SAFEZONE: 1,
    Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT_MATCH.REACH_GOAL: 5,
    Action_NO_EXACT_MATCH.KILL: 0,
}

AGENT_1_DEFAULT_ACTION_ORDER = {
    0, # peu importe où il se situe car quand il y a NO_ACTION, il n'y a que ça
    1, # maximiser le nombre de chevaux sortis
    # TODO : voir le reste de l'ordre des actions
}

AGENT_2_REWARD_TABLE = {
    Action_NO_EXACT_MATCH.NO_ACTION: -1,
    Action_NO_EXACT_MATCH.MOVE_OUT: 1,
    Action_NO_EXACT_MATCH.MOVE_FORWARD: 10,
    Action_NO_EXACT_MATCH.ENTER_SAFEZONE: 1,
    Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT_MATCH.REACH_GOAL: 5,
    Action_NO_EXACT_MATCH.KILL: 0,
}

AGENT_2_DEFAULT_ACTION_ORDER = {
    0, # peu importe où il se situe car quand il y a NO_ACTION, il n'y a que ça
    9, 
    4, 
    7, # maximiser l'avancé de ses pions déjà sortis
    2, 
    # TODO : voir le reste de l'ordre des actions
}

AGENT_3_REWARD_TABLE = {
    Action_NO_EXACT_MATCH.NO_ACTION: -1,
    Action_NO_EXACT_MATCH.MOVE_OUT: 1,
    Action_NO_EXACT_MATCH.MOVE_FORWARD: 1,
    Action_NO_EXACT_MATCH.ENTER_SAFEZONE: 1,
    Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT_MATCH.REACH_GOAL: 1,
    Action_NO_EXACT_MATCH.KILL: 10,
}

AGENT_4_REWARD_TABLE = {
    Action_NO_EXACT_MATCH.NO_ACTION: -1,
    Action_NO_EXACT_MATCH.MOVE_OUT: 1,
    Action_NO_EXACT_MATCH.MOVE_FORWARD: 1,
    Action_NO_EXACT_MATCH.ENTER_SAFEZONE: 10,
    Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT_MATCH.REACH_GOAL: 5,
    Action_NO_EXACT_MATCH.KILL: 0,
}

AGENT_5_REWARD_TABLE = {
    Action_NO_EXACT_MATCH.NO_ACTION: 10,
    Action_NO_EXACT_MATCH.MOVE_OUT: 1,
    Action_NO_EXACT_MATCH.MOVE_FORWARD: 1,
    Action_NO_EXACT_MATCH.ENTER_SAFEZONE: 1,
    Action_NO_EXACT_MATCH.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT_MATCH.REACH_GOAL: 1,
    Action_NO_EXACT_MATCH.KILL: 1,
}