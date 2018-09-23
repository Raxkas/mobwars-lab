from copy import deepcopy

from mob_basket import MobBasket
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
        self._new_basket()

    def next_wave(self):
        self.player.money += int(0.8 * self.mob_basket.income_increase)  # bad simulation of mob-killing money
        self._new_basket()
        self.player.do_limit_mob_stock = True
        self.player.add_time(0.1)  # next_wave
        self._consider_mob_increment()

    def _consider_mob_increment(self):
        self.player.do_limit_mob_stock = False
        self.player.add_time(WAVE_DURATION_SEC - 0.1 - self.player.sec_since_wave_start)

    def _new_basket(self):
        # TODO: create mobwars.mob_counter?
        self.mob_basket = MobBasket()

    def copy(self):
        return deepcopy(self)

    def merge(self, other):
        for mob in other.mob_basket:
            self.buy_mob(mob)

    def buy_mob(self, mob):
        self.player.buy_mob(mob)
        self.mob_basket.buy(mob)

    def buy_basket(self, mob_basket):
        self.mob_basket.merge(mob_basket)
        self.player.buy_basket(mob_basket)
