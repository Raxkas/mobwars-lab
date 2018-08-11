from functools import partial
import itertools

from mobwars.player import Player
from forker import compute_available_branches, Branch


# TODO: fix code repeating

def get_branch_income(branch):
    income = 0
    for kind, count in branch.mob_basket.items():
        income += count * kind.income
    return income


def get_branch_money_cost(branch):
    money_cost = 0
    for kind, count in branch.mob_basket.items():
        money_cost += count * kind.money_cost
    return money_cost


def watch_future_money(branch, waves_forward):
    income = get_branch_income(branch)
    cost = get_branch_money_cost(branch)
    return waves_forward*income - cost


def choice_best_branch(branches, waves_forward):
    key_func = partial(watch_future_money, waves_forward=waves_forward)
    return max(branches, key=key_func)


def compute_next_branch(branch, waves_forward):
    branches = compute_available_branches(branch.player)
    return choice_best_branch(branches, waves_forward)


# TODO: refactoring


def get_tactic_by_waves_forward(waves_forward):
    player = Player()
    player.skip_time_to_wave_end()
    best_branch = Branch(player)
    while waves_forward > 0:
        best_branch = compute_next_branch(best_branch, waves_forward)
        yield best_branch
        best_branch = best_branch.copy()
        best_branch.next_wave()
        waves_forward -= 1


# TODO: optimization by binary search?
def get_tactic_by_necessary_money(necessary_money):
    for waves_forward in itertools.count():
        tactic = tuple(get_tactic_by_waves_forward(waves_forward))
        if tactic[-1].player.money >= necessary_money:
            return tactic
