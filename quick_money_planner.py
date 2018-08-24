from functools import partial
import itertools

from branch import Branch
from forker import compute_available_baskets


# TODO: refactoring


def watch_future_money(mob_basket, waves_forward):
    income = mob_basket.income_increase
    cost = mob_basket.money_cost
    return waves_forward*income - cost


def choice_best_basket(baskets, waves_forward):
    key_func = partial(watch_future_money, waves_forward=waves_forward)
    return max(baskets, key=key_func)


def compute_best_basket(player, waves_forward):
    baskets = compute_available_baskets(player)
    return choice_best_basket(baskets, waves_forward)


def get_tactic_by_waves_forward(waves_forward):
    branch = Branch()
    for waves_forward in range(waves_forward, 0, -1):
        best_basket = compute_best_basket(branch.player, waves_forward)
        branch.buy_basket(best_basket)
        yield branch.copy()
        branch.next_wave()


# TODO: optimization by binary search?
def get_tactic_by_necessary_money(necessary_money):
    for waves_forward in itertools.count(1):
        tactic = tuple(get_tactic_by_waves_forward(waves_forward))
        if tactic[-1].player.money >= necessary_money:
            return tactic
