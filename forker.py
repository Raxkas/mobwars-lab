from functools import lru_cache, partial

from mob_basket import MobBasket


# TODO: player can avoid overflowing of the mob-stack by buying during a wave.
# TODO: iteration method cannot work for big mob-shops


def _generator_with_cache(func):
    @lru_cache(maxsize=None)
    def new_func(*args, **kwargs):
        return tuple(func(*args, **kwargs))
    return new_func


def join_every_basket_with(baskets, main_basket):
    baskets = tuple(map(MobBasket.copy, baskets))
    for basket in baskets:
        basket.merge(main_basket)
    return baskets


@_generator_with_cache
def _compute_available_baskets(power, mob_kinds, ignored_kinds_count=0):
    current_basket = MobBasket()
    if ignored_kinds_count == len(mob_kinds):
        yield current_basket
        return;
    # current_kind_index = ignored_kinds_count
    current_kind_index = -1-ignored_kinds_count
    current_kind = mob_kinds[current_kind_index]
    yield from _compute_available_baskets(power, mob_kinds, ignored_kinds_count + 1)
    while power >= current_kind.power_cost:
        current_basket.buy(current_kind)
        power -= current_kind.power_cost
        baskets = _compute_available_baskets(power, mob_kinds, ignored_kinds_count + 1)
        yield from join_every_basket_with(baskets, current_basket)


# TODO: mob_stock checking is not implemented
def can_buy(player, basket):
    enough_power = player.power >= basket.power_cost
    enough_money = player.money >= basket.money_cost
    return enough_power and enough_money


def compute_available_baskets(player):
    unfiltered = _compute_available_baskets(player.power, player.mob_kinds)
    can_player_buy = partial(can_buy, player)
    result = filter(can_player_buy, unfiltered)
    result = map(MobBasket.copy, result)
    return tuple(result)
