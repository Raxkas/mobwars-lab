from copy import deepcopy

from mobwars.mob import mob_kinds


WAVE_DURATION_SEC = 25


# TODO: non-mob_kinds-oriented mob_stock?
class Player:
    """The player model."""
    waves_since_game_start = 0
    sec_since_wave_start = 0
    hp = 20
    power = 10
    money = 25
    income = 25
    mob_kinds = mob_kinds
    do_limit_mob_stock = True

    def __init__(self):
        """Initialize player."""
        self.mob_stock = {kind: 0 for kind in mob_kinds}
        self._mob_stock_sec = {kind: kind.cooldown - kind.unlock_time for kind in mob_kinds}

    def add_time(self, time_sec):
        """Time passage simulation."""
        self._add_time(time_sec)
        if self.do_limit_mob_stock:
            self._clip_mob_stock()
        while self.sec_since_wave_start >= WAVE_DURATION_SEC:
            self._next_wave()

    def _add_time(self, time_sec):
        """Just increment time and update mobs ignoring stack_size."""
        self.sec_since_wave_start += time_sec
        for kind in mob_kinds:
            self._mob_stock_sec[kind] += time_sec
            while self._mob_stock_sec[kind] >= kind.cooldown:
                self._mob_stock_sec[kind] -= kind.cooldown
                self.mob_stock[kind] += 1

    def _clip_mob_stock(self):
        """Fix mob_stock overflows."""
        for kind in mob_kinds:
            if self.mob_stock[kind] >= kind.stack_size:
                self.mob_stock[kind] = kind.stack_size
                self._mob_stock_sec[kind] = 0

    def _next_wave(self):
        """Make and process wave increment."""
        self.waves_since_game_start += 1
        self.sec_since_wave_start -= WAVE_DURATION_SEC
        self.money += self.income
        self.power = type(self).power

    def copy(self):
        """Make a copy of the player."""
        return deepcopy(self)

    def is_mob_available(self, mob):  # TODO: rename
        """Check the possibility of mob buying."""
        enough_money = mob.money_cost <= self.money
        enough_power = mob.power_cost <= self.power
        enough_count = self.mob_stock[mob] > 0
        return enough_money and enough_power and enough_count

    # TODO: possibility check?
    def buy_mob(self, mob):
        """Buy a mob."""
        self.money -= mob.money_cost
        self.power -= mob.power_cost
        self.mob_stock[mob] -= 1
        self.income += mob.income

    def buy_basket(self, mob_basket):
        """Buy a basket of mobs."""
        for mob in mob_basket:
            self.buy_mob(mob)
