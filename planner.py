from mobwars.player import Player
from forker import compute_available_branches, Branch


def choice_best_branch(branches):
    return max(branches, key=lambda branch: branch.player.income)


def compute_next_branch(branch):
    branches = compute_available_branches(branch.player)
    return choice_best_branch(branches)


def next_wave(branch):
    new_income = 0
    for mob_kind, count in branch.mob_basket.items():
        new_income += count * mob_kind.income
    branch = Branch(branch.player)  # mob_basket clearing
    branch.player.money += int(0.8*new_income)  # bad simulation of mob-killing money
    branch.player.next_wave()
    branch.player.skip_time_to_wave_end()
    return branch


def get_tactic():
    player = Player()
    player.skip_time_to_wave_end()
    best_branch = Branch(player)
    while True:
        best_branch = compute_next_branch(best_branch)
        yield best_branch
        best_branch = next_wave(best_branch)
