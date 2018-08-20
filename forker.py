from functools import partial

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
        # TODO: collections.counter or mobwars.mob_counter
        self._new_basket()

    def _new_basket(self):
        self.mob_basket = {kind: 0 for kind in self.player.mob_kinds}
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

    def buy(self, mob):
        self.player.buy(mob)
        self.mob_basket[mob] += 1
        self.money_cost += mob.money_cost
        self.income_increase += mob.income


# TODO: iteration method cannot work for big mob-shops


# TODO: refactoring


@lru_cache(maxsize=None)
def _get_all_possible_mob_baskets(power, available_mobs):
    if not available_mobs:
        return [()]
    mob, available_mobs = available_mobs[-1], available_mobs[:-1]
    result = []
    basket = ()
    while power >= 0:
        variants = _get_all_possible_mob_baskets(power, available_mobs)
        if basket:
            variants = map(basket.__add__, variants)
        result.extend(variants)
        power -= mob.power_cost
        basket += (mob,)
    return tuple(result)


def __test(func):
    from time import time as get_current_time

    start_time = get_current_time()
    result = func(Player.power, Player.mob_kinds)
    execution_time = get_current_time() - start_time

    cache_info = func.cache_info()
    func.cache_clear()

    result_length = len(result)

    def sort_basket(basket):
        return tuple(sorted(basket, key=lambda kind: kind.name))

    result = set(map(sort_basket, result))
    real_result_length = len(result)

    print("Name:", func.__name__)
    print("Execution time:", execution_time)
    print("Cache info:", cache_info)
    print("Result length:", result_length)
    if result_length == real_result_length:
        print("No basket repeating.")
    else:
        print("There is basket repeating.", end=' ')
        print("Real length is", real_result_length, end='.\n')


if __name__ == "__main__":
    __test(_get_all_possible_mob_baskets)
else:
    raise ImportError
