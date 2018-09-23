from functools import partial

from mobwars.player import Player, WAVE_DURATION_SEC


# TODO: player can avoid overflowing of the mob-stack by buying during a wave.
class Branch:
    """
    Describes purchases for the wave.

    Consists of a mob-basket and a player's model.
    The mob-basket displays the number of purchased mobs: {mob_class: purchases_count}.
    The player's model displays the player's state after buying.
    """

    def __init__(self, player=None):
        if player is None:
            self.player = Player()
        else:
            self.player = player.copy()
        self._consider_mob_increment()
        # TODO: collections.counter or mobwars.mob_counter
        self._new_basket()

    def next_wave(self):
        self.player.money += int(0.8 * self.income_increase)  # bad simulation of mob-killing money
        self._new_basket()
        self.player.do_limit_mob_stock = True
        self.player.add_time(0.1)  # next_wave
        self._consider_mob_increment()

    def _consider_mob_increment(self):
        self.player.do_limit_mob_stock = False
        self.player.add_time(WAVE_DURATION_SEC - 0.1 - self.player.sec_since_wave_start)

    def _new_basket(self):
        self.mob_basket = {kind: 0 for kind in self.player.mob_kinds}
        self.income_increase = 0
        self.money_cost = 0

    # TODO: use copy module?
    def copy(self):
        copy = self.__class__(self.player)
        copy.mob_basket = self.mob_basket.copy()
        copy.money_cost = self.money_cost
        copy.income_increase = self.income_increase
        return copy

    def buy(self, mob):
        self.player.buy(mob)
        self.mob_basket[mob] += 1
        self.money_cost += mob.money_cost
        self.income_increase += mob.income


# TODO: iteration method requires optimization and it cannot work for big mob-shops

def get_forks_consider_new_mob(branch, mob):
    branch = branch.copy()
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
