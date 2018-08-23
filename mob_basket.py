

# TODO: player can avoid overflowing of the mob-stack by buying during a wave.
# TODO: immutable version?
class MobBasket:
    """Purchases for the wave. """

    __slots__ = ("mobs", "income_increase", "money_cost", "power_cost")

    def __init__(self):
        self.mobs = ()
        self.income_increase = 0
        self.money_cost = 0
        self.power_cost = 0

    # TODO: use copy module?
    def copy(self):
        copy = self.__class__()
        copy.mobs = self.mobs
        copy.income_increase = self.income_increase
        copy.money_cost = self.money_cost
        copy.power_cost = self.power_cost
        return copy

    def merge(self, other):
        self.mobs += other.mobs
        self.income_increase += other.income_increase
        self.money_cost += other.money_cost
        self.power_cost += other.power_cost

    def buy(self, mob):
        # self.mobs[mob] += 1
        self.mobs += (mob,)
        self.income_increase += mob.income
        self.money_cost += mob.money_cost
        self.power_cost += mob.power_cost
