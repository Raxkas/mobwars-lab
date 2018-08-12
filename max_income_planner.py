from forker import compute_available_branches, Branch


def choice_best_branch(branches):
    return max(branches, key=lambda branch: branch.player.income)


def compute_next_branch(branch):
    branches = compute_available_branches(branch.player)
    return choice_best_branch(branches)


def get_max_income_tactic():
    best_branch = Branch()
    while True:
        best_branch = compute_next_branch(best_branch)
        yield best_branch.copy()
        best_branch.next_wave()
