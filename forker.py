from functools import lru_cache


# TODO: rename to "Variant"?
class Branch:
    def __init__(self, player):
        # TODO: collections.counter
        mob_basket = {kind: 0 for kind in player.mob_kinds}
        self.mob_basket = mob_basket
        self.player = player.copy()

    def next_wave(self):
        new_income = 0
        for mob_kind, count in self.mob_basket.items():
            new_income += count * mob_kind.income
        self.mob_basket = Branch(self.player).mob_basket
        self.player.money += int(0.8 * new_income)  # bad simulation of mob-killing money
        self.player.next_wave()
        self.player.skip_time_to_wave_end()

    def copy(self):
        mob_basket, player = self.mob_basket.copy(), self.player.copy()
        copy = self.__class__(player)
        copy.mob_basket = mob_basket
        return copy

    def buy(self, mob):
        self.player.buy(mob)
        self.mob_basket[mob] += 1


def get_forks_consider_new_mob(branch, mob):
    while branch.player.is_mob_available(mob):
        branch = branch.copy()
        branch.buy(mob)
        yield branch


def extend_branches_consider_new_mob(branches, mob):
    for branch in tuple(branches):
        fork_extensions = get_forks_consider_new_mob(branch, mob)
        branches.extend(fork_extensions)


# TODO: maybe recovery from player?
# TODO: maybe history in player?
# TODO: time system?
def compute_available_branches(player):
    branch = Branch(player)
    branches = [branch]
    for mob in player.mob_kinds:
        extend_branches_consider_new_mob(branches, mob)
    return branches
