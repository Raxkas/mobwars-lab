from mobwars.mob import mob_kinds


WAVE_DURATION_SEC = 25


class Player:
    hp = 20
    power = 10
    money = 25
    income = 25
    mob_kinds = mob_kinds
    _mob_stock_sec = {kind: kind.cooldown - kind.unlock_time for kind in mob_kinds}
    mob_stock = {kind: 0 for kind in mob_kinds}

    # TODO: design time system and refactor that
    # TODO: refactoring

    def skip_time_to_wave_end(self):
        self.add_time(WAVE_DURATION_SEC)

    def add_time(self, time_sec):
        for kind in mob_kinds:
            self._mob_stock_sec[kind] += time_sec
            if self._mob_stock_sec[kind]//kind.cooldown >= kind.stack_size:
                self._mob_stock_sec[kind] = kind.stack_size * kind.cooldown
            self.mob_stock[kind] = self._mob_stock_sec[kind] // kind.cooldown

    def next_wave(self):
        self.money += self.income
        self.power = 10

    # TODO: refactoring
    def copy(self):
        copy = self.__class__()
        for field in "hp power money income mob_kinds _mob_stock_sec mob_stock".split():
            value = getattr(self, field)
            if hasattr(value, "copy"):
                value = value.copy()
            setattr(copy, field, value)
        return copy

    def is_mob_available(self, mob):
        enough_money = mob.money_cost <= self.money
        enough_power = mob.power_cost <= self.power
        enough_count = self.mob_stock[mob] > 0
        return enough_money and enough_power and enough_count

    # TODO: possibility check?
    def buy(self, mob):
        self.money -= mob.money_cost
        self.power -= mob.power_cost
        self.mob_stock[mob] -= 1
        self.income += mob.income
