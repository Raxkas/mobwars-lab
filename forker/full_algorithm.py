from collections import namedtuple

from forker.algorithm_base import BaseAlgorithm
from forker.nomoney_algorithm import NoMoneyAlgorithm


class FullAlgorithm(NoMoneyAlgorithm):
    __slots__ = ()

    class _PlayerData(namedtuple("_PlayerData", "available_mobs power money"), BaseAlgorithm._PlayerData):
        __slots__ = ()

    @staticmethod
    def _filter_result(unfiltered, player):
        return unfiltered

    def _can_buy_current_kind(self):
        enough_money = self._player_data.money >= self._current_mob.money_cost
        return enough_money and super()._can_buy_current_kind()

    def _buy_current_kind(self):
        super()._buy_current_kind()
        new_money = self._player_data.money - self._current_mob.money_cost
        self._player_data = self._player_data._replace(money=new_money)
