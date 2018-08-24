from branch import Branch
from forker import compute_available_baskets


def choice_best_basket(baskets):
    return max(baskets, key=lambda basket: basket.income_increase)


def compute_best_basket(player):
    baskets = compute_available_baskets(player)
    return choice_best_basket(baskets)


def get_max_income_tactic():
    branch = Branch()
    while True:
        best_basket = compute_best_basket(branch.player)
        branch.buy_basket(best_basket)
        yield branch.copy()
        branch.next_wave()
