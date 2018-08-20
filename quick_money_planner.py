from functools import partial
import itertools

from forker import compute_available_branches, Branch


# TODO: refactoring


def watch_future_money(branch, waves_forward):
    income = branch.income_increase
    cost = branch.money_cost
    return waves_forward*income - cost


def choice_best_branch(branches, waves_forward):
    key_func = partial(watch_future_money, waves_forward=waves_forward)
    return max(branches, key=key_func)


def compute_next_branch(branch, waves_forward):
    branches = compute_available_branches(branch.player)
    return choice_best_branch(branches, waves_forward)


def get_tactic_by_waves_forward(waves_forward):
    best_branch = Branch()
    for waves_forward in range(waves_forward, 0, -1):
        best_branch = compute_next_branch(best_branch, waves_forward)
        yield best_branch.copy()
        best_branch.next_wave()


# TODO: optimization by binary search?
def get_tactic_by_necessary_money(necessary_money):
    for waves_forward in itertools.count(1):
        tactic = tuple(get_tactic_by_waves_forward(waves_forward))
        if tactic[-1].player.money >= necessary_money:
            return tactic
