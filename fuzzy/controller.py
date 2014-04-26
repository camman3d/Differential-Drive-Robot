__author__ = 'josh'


MoveForward = 1, 0, 0
TurnLeft = 0, 1, 0
TurnRight = 0, 0, 1
DoNothing = 0, 0, 0


# Fuzzy rules

def nothing(fuzzy_vars):
    if fuzzy_vars[0] is None and fuzzy_vars[1] is None:
        return TurnLeft


def dest_middle(fuzzy_vars):
    if fuzzy_vars[1] is not None and 0.3 < fuzzy_vars[1] < 0.7 and fuzzy_vars[2] < 0.5:
        return MoveForward


def dest_left(fuzzy_vars):
    if fuzzy_vars[1] is not None and fuzzy_vars[1] <= 0.3 and fuzzy_vars[2] < 0.5:
        return TurnLeft


def dest_right(fuzzy_vars):
    if fuzzy_vars[1] is not None and fuzzy_vars[1] >= 0.7 and fuzzy_vars[2] < 0.5:
        return TurnRight


def obst_midleft(fuzzy_vars):
    if fuzzy_vars[0] is not None and 0.2 < fuzzy_vars[0] <= 0.5 < fuzzy_vars[2]:
        return TurnRight


def obst_midright(fuzzy_vars):
    if fuzzy_vars[0] is not None and 0.5 < fuzzy_vars[0] < 0.8 and fuzzy_vars[2] > 0.5:
        return TurnLeft


def obst_left(fuzzy_vars):
    if fuzzy_vars[0] is not None and fuzzy_vars[0] <= 0.2 and fuzzy_vars[2] > 0.5:
        return MoveForward


def obst_right(fuzzy_vars):
    if fuzzy_vars[0] is not None and fuzzy_vars[0] >= 0.8 and fuzzy_vars[2] > 0.5:
        return MoveForward


# Rule processor

all_rules = [nothing, dest_left, dest_middle, dest_right, obst_left, obst_midleft, obst_midright, obst_right]

def processor(fuzzy_vars, rules):
    result = 0, 0, 0
    for rule in rules:
        r = rule(fuzzy_vars)
        if r is None:
            r = DoNothing
        result = result[0] + r[0], result[1] + r[1], result[2] + r[2]
    return result
