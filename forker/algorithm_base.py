from collections import namedtuple
from functools import lru_cache

from mob_basket import ImmutableMobBasket


def _returned_value_to_tuple(func):
    def new_func(*args, **kwargs):
        return tuple(func(*args, **kwargs))
    return new_func


class _PlayerData(namedtuple("_PlayerData", ["available_mobs"])):
    __slots__ = ()

    @classmethod
    def create_by_player(cls, player):
        args = cls._get_fields_by_player(player)
        return cls(*args)

    @staticmethod
    def _get_available_mobs_by_player(player):
        available_mobs = filter(lambda pair: pair[1] > 0, player.mob_stock.items())
        available_mobs = sorted(available_mobs, key=lambda pair: pair[0].power_cost, reverse=True)
        return tuple(available_mobs)

    @classmethod
    def _get_fields_by_player(cls, player):
        exceptions = {
            "available_mobs": cls._get_available_mobs_by_player
        }
        for field_name in cls._fields:
            if field_name in exceptions.keys():
                func = exceptions[field_name]
                yield func(player)
            else:
                yield getattr(player, field_name)


class BaseAlgorithm:
    __slots__ = ("_player_data", "_current_mob", "_current_mob_available", "_mob_basket")
    _PlayerData = _PlayerData

    def __init__(self, player_data):
        if not isinstance(player_data, self._PlayerData):
            raise TypeError
        self._player_data = player_data
        self._mob_basket = ImmutableMobBasket.default_instance
        self._current_mob, self._current_mob_available = self._player_data.available_mobs[0]
        other_mobs = self._player_data.available_mobs[1:]
        self._player_data = self._player_data._replace(available_mobs=other_mobs)

    @classmethod
    def call(cls, player):
        player_data = cls._PlayerData.create_by_player(player)
        unfiltered = cls._compute_available_baskets(player_data)
        result = cls._filter_result(unfiltered, player)
        return tuple(result)

    @staticmethod
    def _filter_result(unfiltered, player):
        player_power = player.power
        player_money = player.money

        def condition(basket):
            return basket.power_cost <= player_power and basket.money_cost <= player_money
        return filter(condition, unfiltered)

    @classmethod
    @lru_cache(maxsize=256)
    @_returned_value_to_tuple
    def _compute_available_baskets(cls, player_data):
        if not player_data.available_mobs:
            yield ImmutableMobBasket.default_instance
            return;
        alg = cls(player_data)
        yield from cls._compute_available_baskets(alg._player_data)
        while alg._can_buy_current_kind():
            alg._buy_current_kind()
            baskets = cls._compute_available_baskets(alg._player_data)
            yield from alg._get_completed_baskets(baskets)

    def _get_completed_baskets(self, baskets):
        get_completed_basket = self._mob_basket.__add__
        return map(get_completed_basket, baskets)

    def _can_buy_current_kind(self):
        mob_is_available = self._current_mob_available > 0
        return mob_is_available

    def _buy_current_kind(self):
        self._current_mob_available -= 1
        self._mob_basket = self._mob_basket.buy(self._current_mob)
