from functools import lru_cache, partial

from mobwars.player import Player


class Branch:
    def __init__(self, player=None):
        if player is None:
            self.player = Player()
            self.player.skip_time_to_wave_end()
        else:
            self.player = player.copy()
        # TODO: collections.counter
        mob_basket = {kind: 0 for kind in self.player.mob_kinds}
        self.mob_basket = mob_basket

    def next_wave(self):
        new_income = 0
        for mob_kind, count in self.mob_basket.items():
            new_income += count * mob_kind.income
        self.mob_basket = Branch(self.player).mob_basket
        self.player.money += int(0.8 * new_income)  # bad simulation of mob-killing money
        self.player.next_wave()
        self.player.skip_time_to_wave_end()

    def copy(self):
        mob_basket, player = self.mob_basket.copy(), self.player.copy()
        copy = self.__class__(player)
        copy.mob_basket = mob_basket
        return copy

    def buy(self, mob):
        self.player.buy(mob)
        self.mob_basket[mob] += 1


# TODO: iteration method requires optimization and it cannot work for big mob-shops

def get_forks_consider_new_mob(branch, mob):
    while branch.player.is_mob_available(mob):
        branch.buy(mob)
        yield branch.copy()


def extend_branches_consider_new_mob(branches, mob):
    extend_branches = branches.extend
    for branch in tuple(branches):
        forks = get_forks_consider_new_mob(branch, mob)
        extend_branches(forks)


def compute_available_branches(player):
    branch = Branch(player)
    result = [branch]
    extend_result_consider_new_mob = partial(extend_branches_consider_new_mob, branches=result)
    for mob in player.mob_kinds:
        extend_result_consider_new_mob(mob=mob)
    return result
