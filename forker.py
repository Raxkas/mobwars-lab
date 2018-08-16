from functools import lru_cache, partial

from mobwars.player import Player


class Branch:
    def __init__(self, player=None):
        if player is None:
            self.player = Player()
            self.player.skip_time_to_wave_end()
        else:
            self.player = player.copy()
        # TODO: collections.counter or mobwars.mob_counter
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
