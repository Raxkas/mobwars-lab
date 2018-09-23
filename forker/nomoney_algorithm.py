from collections import namedtuple

from forker.algorithm_base import BaseAlgorithm


class NoMoneyAlgorithm(BaseAlgorithm):
    __slots__ = ()

    class _PlayerData(namedtuple("_PlayerData", "available_mobs power"), BaseAlgorithm._PlayerData):
        __slots__ = ()

    @staticmethod
    def _filter_result(unfiltered, player):
        def condition(basket):
            return basket.money_cost <= player.money
        result = filter(condition, unfiltered)
        return result

    def _can_buy_current_kind(self):
        enough_power = self._player_data.power >= self._current_mob.power_cost
        return enough_power and super()._can_buy_current_kind()

    def _buy_current_kind(self):
        super()._buy_current_kind()
        new_power = self._player_data.power - self._current_mob.power_cost
        self._player_data = self._player_data._replace(power=new_power)
