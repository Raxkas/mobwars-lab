class MobBasket:
    """Purchases for the wave."""

    __slots__ = ("_mobs", "income_increase", "money_cost", "power_cost")

    def __init__(self):
        self._mobs = ()
        self.income_increase = 0
        self.money_cost = 0
        self.power_cost = 0

    def __iter__(self):
        return iter(self._mobs)

    # TODO: use copy module?
    def copy(self):
        copy = self.__class__()
        copy._mobs = self._mobs
        copy.income_increase = self.income_increase
        copy.money_cost = self.money_cost
        copy.power_cost = self.power_cost
        return copy

    def merge(self, other):
        self._mobs += other.mobs
        self.income_increase += other.income_increase
        self.money_cost += other.money_cost
        self.power_cost += other.power_cost

    def buy(self, mob):
        self._mobs += (mob,)
        self.income_increase += mob.income
        self.money_cost += mob.money_cost
        self.power_cost += mob.power_cost
