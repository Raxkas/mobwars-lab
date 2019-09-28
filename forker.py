from functools import lru_cache

from mob_basket import ImmutableMobBasket


def compute_available_baskets(player):
    result_ignoring_money = _compute_available_baskets_ignoring_money(
        available_mobs=_get_available_mobs_by_player(player),
        power=player.power
    )
    result = filter(
        lambda basket: basket.money_cost <= player.money,
        result_ignoring_money
    )
    return tuple(result)


def _get_available_mobs_by_player(player):
    available_mobs = filter(lambda pair: pair[1] > 0, player.mob_stock.items())
    available_mobs = sorted(available_mobs, key=lambda pair: pair[0].power_cost, reverse=True)
    return tuple(available_mobs)


def _convert_generator_to_tuple(function):
    def new_function(*args, **kwargs):
        return tuple(function(*args, **kwargs))
    new_function.__name__ = function.__name__
    new_function.__doc__ = function.__doc__
    return new_function


@lru_cache(maxsize=256)
@_convert_generator_to_tuple
def _compute_available_baskets_ignoring_money(available_mobs, power):
    if not available_mobs:
        yield ImmutableMobBasket.default_instance
        return
    mob_basket = ImmutableMobBasket.default_instance
    (current_mob, current_mob_available) = available_mobs[0]
    available_mobs = available_mobs[1:]
    yield from _compute_available_baskets_ignoring_money(available_mobs, power)
    while current_mob_available > 0 and power >= current_mob.power_cost:
        current_mob_available -= 1
        power -= current_mob.power_cost
        mob_basket = mob_basket.buy(current_mob)
        baskets = _compute_available_baskets_ignoring_money(
            available_mobs, power
        )
        yield from map(mob_basket.__add__, baskets)
