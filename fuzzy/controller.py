__author__ = 'josh'


MoveForward = 1, 0, 0
TurnLeft = 0, 1, 0
TurnRight = 0, 0, 1
DoNothing = 0, 0, 0


# Fuzzy rules

def nothing(fuzzy_vars):
    return fuzzy_vars[0] is None and fuzzy_vars[1] is None


def dest_middle(fuzzy_vars):
    return fuzzy_vars[1] is not None and 0.3 < fuzzy_vars[1] < 0.7 and fuzzy_vars[2] < 0.75


def dest_left(fuzzy_vars):
    return fuzzy_vars[1] is not None and fuzzy_vars[1] <= 0.3 and fuzzy_vars[2] < 0.75


def dest_right(fuzzy_vars):
    return fuzzy_vars[1] is not None and fuzzy_vars[1] >= 0.7 and fuzzy_vars[2] < 0.75


# def obst_left(fuzzy_vars):
#     return fuzzy_vars[0] is not None and fuzzy_vars[0] < 0.5 < fuzzy_vars[2]
#
#
# def obst_right(fuzzy_vars):
#     return fuzzy_vars[0] is not None and fuzzy_vars[0] > 0.5 and fuzzy_vars[2] > 0.5
#
#
# def obst_midleft(fuzzy_vars):
#     return fuzzy_vars[0] is not None and 0.2 < fuzzy_vars[0] <= 0.5 < fuzzy_vars[2]
#
#
# def obst_midright(fuzzy_vars):
#     return fuzzy_vars[0] is not None and 0.5 < fuzzy_vars[0] < 0.8 and fuzzy_vars[2] > 0.5


def obst(fuzzy_vars):
    return fuzzy_vars[0] is not None and fuzzy_vars[2] > 0.75


# def obst_left(fuzzy_vars):
#     return fuzzy_vars[0] is not None and fuzzy_vars[0] <= 0.2 and fuzzy_vars[2] > 0.5


# def obst_right(fuzzy_vars):
#     return fuzzy_vars[0] is not None and fuzzy_vars[0] >= 0.8 and fuzzy_vars[2] > 0.5


# Rule processor

# all_rules = [nothing, dest_left, dest_middle, dest_right, obst_left, obst_midleft, obst_midright, obst_right]
#
#
# def processor(fuzzy_vars, rules):
#     result = 0, 0, 0
#     for rule in rules:
#         r = rule(fuzzy_vars)
#         if r is None:
#             r = DoNothing
#         result = result[0] + r[0], result[1] + r[1], result[2] + r[2]
#     return result


def get_behavior(fuzzy_vars, last_behavior):
    if nothing(fuzzy_vars):
        if last_behavior <= 0:
            return last_behavior - 1
        if 4 <= last_behavior <= 7:
            return last_behavior + 2
        if last_behavior >= 8:
            return last_behavior

    if dest_middle(fuzzy_vars):
        return 1
    if dest_left(fuzzy_vars):
        return 2
    if dest_right(fuzzy_vars):
        return 3

    if obst(fuzzy_vars):
        if 4 <= last_behavior <= 5:
            return last_behavior
        if last_behavior == 8:
            return 4
        if last_behavior == 9:
            return 5
        return 4

    return 0