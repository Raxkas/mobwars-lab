from mobwars.player import Player
from forker import compute_available_branches, Branch


def choice_best_branch(branches):
    return max(branches, key=lambda branch: branch.player.income)


def compute_next_branch(branch):
    branches = compute_available_branches(branch.player)
    return choice_best_branch(branches)


def get_max_income_tactic():
    player = Player()
    player.skip_time_to_wave_end()
    best_branch = Branch(player)
    while True:
        best_branch = compute_next_branch(best_branch)
        yield best_branch
        best_branch = best_branch.copy()
        best_branch.next_wave()
