from collections import Counter
from functools import lru_cache, partial

from mobwars.player import Player


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
            self.player.skip_time_to_wave_end()
        else:
            self.player = player.copy()
        self._new_basket()

    def _new_basket(self):
        # TODO: create mobwars.mob_counter?
        self.mob_basket = Counter({kind: 0 for kind in self.player.mob_kinds})
        self.income_increase = 0
        self.money_cost = 0

    def next_wave(self):
        self.player.money += int(0.8 * self.income_increase)  # bad simulation of mob-killing money
        self._new_basket()
        self.player.next_wave()
        self.player.skip_time_to_wave_end()

    # TODO: use copy module?
    def copy(self):
        copy = self.__class__(self.player)
        copy.mob_basket = self.mob_basket.copy()
        copy.money_cost = self.money_cost
        copy.income_increase = self.income_increase
        return copy

    def merge(self, other):
        for mob in other.mob_basket.elements():
            self.buy(mob)

    def buy(self, mob):
        self.player.buy(mob)
        self.mob_basket[mob] += 1
        self.money_cost += mob.money_cost
        self.income_increase += mob.income


# TODO: iteration method cannot work for big mob-shops


# TODO: refactoring
# TODO: immutable branch?

def _compute_available_branches(player, ignored_kinds_count=0):
    main_branch = Branch(player)
    mob_kinds = player.mob_kinds
    if ignored_kinds_count == len(mob_kinds):
        yield main_branch
        return None
    current_kind_index = ignored_kinds_count
    current_kind = mob_kinds[current_kind_index]
    yield from _compute_available_branches(main_branch.player, ignored_kinds_count + 1)
    while main_branch.player.is_mob_available(current_kind):
        main_branch.buy(current_kind)
        branches = tuple(_compute_available_branches(main_branch.player, ignored_kinds_count + 1))
        for branch in branches:
            branch.merge(main_branch)
        yield from branches


def compute_available_branches(player):
    return tuple(_compute_available_branches(player))
