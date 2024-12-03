from ludo_env.action import Action_NO_EXACT, Action_EXACT


# ------------------- REWARD TABLES -------------------

REWARD_TABLE_MOVE_OUT_NO_EXACT = {
    Action_NO_EXACT.NO_ACTION: -1,
    Action_NO_EXACT.MOVE_OUT: 20,
    Action_NO_EXACT.MOVE_OUT_AND_KILL: 10,
    Action_NO_EXACT.MOVE_FORWARD: 5,
    Action_NO_EXACT.ENTER_SAFEZONE: 15,
    Action_NO_EXACT.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT.REACH_GOAL: 10,
    Action_NO_EXACT.KILL: 30,
}  # TODO faudrait que les sommes répartis soient égales ?

REWARD_TABLE_MOVE_OUT_EXACT = {
    Action_EXACT.NO_ACTION: -1,
    Action_EXACT.MOVE_OUT: 20,
    Action_EXACT.MOVE_OUT_AND_KILL: 10,

    Action_EXACT.MOVE_FORWARD: 5,
    Action_EXACT.REACH_PIED_ESCALIER: 15,
    Action_EXACT.AVANCE_RECULE_PIED_ESCALIER: 1,
    Action_EXACT.MOVE_IN_SAFE_ZONE: 5,

    Action_EXACT.REACH_GOAL: 10,
    Action_EXACT.KILL: 30,
}

def get_reward_table(mode_pied_escalier):
    if mode_pied_escalier == "not_exact":
        return REWARD_TABLE_MOVE_OUT_NO_EXACT
    elif mode_pied_escalier == "exact":
        return REWARD_TABLE_MOVE_OUT_EXACT
    else:
        raise ValueError(f"mode_pied_escalier should be 'not_exact' or 'exact', not {mode_pied_escalier}")

# ------------------- DEFAULT ACTION ORDER TABLES -------------------

def get_default_action_order(nb_chevaux, mode_pied_escalier):
    # TODO : scénario c'est toujours le premier cheval qui bouge...

    result = [0] # commun aux 2 Action 
    # favoriser move out 
    result.append(1)  # commun aux 2 Action 
    result.append(2)  # commun aux 2 Action

    if mode_pied_escalier == "not_exact":
        len_ajout = len(Action_NO_EXACT) - 3
        # puis tuer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.KILL.value + i*len_ajout)
        # puis atteindre objectif
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.REACH_GOAL.value + i*len_ajout)
        # mettre pion en sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.ENTER_SAFEZONE.value + i*len_ajout)
        # ensuite avancer dans sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.MOVE_IN_SAFE_ZONE.value + i*len_ajout)
        # enfin juste simplement avancer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.MOVE_FORWARD.value + i*len_ajout)


    elif mode_pied_escalier == "exact":
        len_ajout = len(Action_EXACT) - 3
        # puis tuer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.KILL.value + i*len_ajout)
        # puis atteindre objectif
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.REACH_GOAL.value + i*len_ajout)
        # mettre pion en sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.REACH_PIED_ESCALIER.value + i*len_ajout)
        # avancer pres du pied
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.AVANCE_RECULE_PIED_ESCALIER.value + i*len_ajout)
        # ensuite avancer dans sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.MOVE_IN_SAFE_ZONE.value + i*len_ajout)
        # enfin juste simplement avancer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.MOVE_FORWARD.value + i*len_ajout)
    else:
        raise ValueError(f"mode_pied_escalier should be 'not_exact' or 'exact', not {mode_pied_escalier}")
    return result 

# ## WIP : TODO les différents agents 
# '''
# agent 0 : random
# agent 1 : maximise le nombre de chevaux sortis
# agent 2 : maximise l'avancé de ses pions déjà sortis
# agent 3 : aime tuer les pions des autres
# agent 4 : aime mettre en sécurité ses pions
# agent 5 : aime bouger le moins possible
# agent 6 : aime protéger ses pions # TODO : à implémenter quand on aura les actions protect
# '''

# # TODO : là c'est des tables pour 2 joueurs / 2 chevaux
# # faire en sorte d'avoir des fonctions pour nb joueurs / nb chevaux

# AGENT_0_REWARD_TABLE = {
#     Action_NO_EXACT.NO_ACTION: -1,
#     Action_NO_EXACT.MOVE_OUT: 1,
#     Action_NO_EXACT.MOVE_FORWARD: 1,
#     Action_NO_EXACT.ENTER_SAFEZONE: 1,
#     Action_NO_EXACT.MOVE_IN_SAFE_ZONE: 1,
#     Action_NO_EXACT.REACH_GOAL: 1,
#     Action_NO_EXACT.KILL: 1,
# }

# # TODO : si agent 0 : faire un random pour order

# AGENT_1_REWARD_TABLE = {
#     Action_NO_EXACT.NO_ACTION: -1,
#     Action_NO_EXACT.MOVE_OUT: 10,
#     Action_NO_EXACT.MOVE_FORWARD: 1,
#     Action_NO_EXACT.ENTER_SAFEZONE: 1,
#     Action_NO_EXACT.MOVE_IN_SAFE_ZONE: 1,
#     Action_NO_EXACT.REACH_GOAL: 5,
#     Action_NO_EXACT.KILL: 0,
# }

# AGENT_1_DEFAULT_ACTION_ORDER = {
#     0, # peu importe où il se situe car quand il y a NO_ACTION, il n'y a que ça
#     1, # maximiser le nombre de chevaux sortis
#     # TODO : voir le reste de l'ordre des actions
# }

# AGENT_2_REWARD_TABLE = {
#     Action_NO_EXACT.NO_ACTION: -1,
#     Action_NO_EXACT.MOVE_OUT: 1,
#     Action_NO_EXACT.MOVE_FORWARD: 10,
#     Action_NO_EXACT.ENTER_SAFEZONE: 1,
#     Action_NO_EXACT.MOVE_IN_SAFE_ZONE: 1,
#     Action_NO_EXACT.REACH_GOAL: 5,
#     Action_NO_EXACT.KILL: 0,
# }

# AGENT_2_DEFAULT_ACTION_ORDER = {
#     0, # peu importe où il se situe car quand il y a NO_ACTION, il n'y a que ça
#     9, 
#     4, 
#     7, # maximiser l'avancé de ses pions déjà sortis
#     2, 
#     # TODO : voir le reste de l'ordre des actions
# }

# AGENT_3_REWARD_TABLE = {
#     Action_NO_EXACT.NO_ACTION: -1,
#     Action_NO_EXACT.MOVE_OUT: 1,
#     Action_NO_EXACT.MOVE_FORWARD: 1,
#     Action_NO_EXACT.ENTER_SAFEZONE: 1,
#     Action_NO_EXACT.MOVE_IN_SAFE_ZONE: 1,
#     Action_NO_EXACT.REACH_GOAL: 1,
#     Action_NO_EXACT.KILL: 10,
# }

# AGENT_4_REWARD_TABLE = {
#     Action_NO_EXACT.NO_ACTION: -1,
#     Action_NO_EXACT.MOVE_OUT: 1,
#     Action_NO_EXACT.MOVE_FORWARD: 1,
#     Action_NO_EXACT.ENTER_SAFEZONE: 10,
#     Action_NO_EXACT.MOVE_IN_SAFE_ZONE: 1,
#     Action_NO_EXACT.REACH_GOAL: 5,
#     Action_NO_EXACT.KILL: 0,
# }

# AGENT_5_REWARD_TABLE = {
#     Action_NO_EXACT.NO_ACTION: 10,
#     Action_NO_EXACT.MOVE_OUT: 1,
#     Action_NO_EXACT.MOVE_FORWARD: 1,
#     Action_NO_EXACT.ENTER_SAFEZONE: 1,
#     Action_NO_EXACT.MOVE_IN_SAFE_ZONE: 1,
#     Action_NO_EXACT.REACH_GOAL: 1,
#     Action_NO_EXACT.KILL: 1,
# }


# # TODO reward observation : si gagner alors recevoir plein de reward