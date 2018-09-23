from collections import namedtuple
from copy import deepcopy


class MobBasket:
    """Purchases for the wave."""

    __slots__ = ("mobs", "income_increase", "money_cost", "power_cost")

    def __init__(self):
        self.mobs = ()
        self.income_increase = 0
        self.money_cost = 0
        self.power_cost = 0

    def __iter__(self):
        return iter(self.mobs)

    def copy(self):
        return deepcopy(self)

    def merge(self, other):
        self.mobs += other.mobs
        self.income_increase += other.income_increase
        self.money_cost += other.money_cost
        self.power_cost += other.power_cost

    def buy(self, mob):
        self.mobs += (mob,)
        self.income_increase += mob.income
        self.money_cost += mob.money_cost
        self.power_cost += mob.power_cost


_ImmutableMobBasket = namedtuple("_ImmutableMobBasket", "mobs, income_increase, money_cost, power_cost")


class ImmutableMobBasket(_ImmutableMobBasket):
    """Purchases for the wave."""

    __slots__ = ()

    default_instance = None

    def __iter__(self):
        return iter(self.mobs)

    def __add__(self, other):
        return type(self)(
            mobs=self.mobs+other.mobs,
            income_increase=self.income_increase+other.income_increase,
            money_cost=self.money_cost+other.money_cost,
            power_cost=self.power_cost+other.power_cost
        )

    def buy(self, mob):
        return type(self)(
            mobs=self.mobs+(mob,),
            income_increase=self.income_increase+mob.income,
            money_cost=self.money_cost+mob.money_cost,
            power_cost=self.power_cost+mob.power_cost
        )


ImmutableMobBasket.default_instance = ImmutableMobBasket(
    mobs=(),
    income_increase=0,
    money_cost=0,
    power_cost=0
)
