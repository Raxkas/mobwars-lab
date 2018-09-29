from collections import Counter
from time import time as get_current_time

from mobwars.player import Player

from forker import compute_available_baskets, NoMoneyAlgorithm
from max_income_planner import get_max_income_tactic
from quick_money_planner import get_tactic_by_necessary_money


def print_tactic(tactic):
    for branch in tactic:
        basket = branch.mob_basket.copy()
        player = branch.player.copy()
        mobs_names = map(lambda mob_kind: mob_kind.name, basket)
        basket = Counter(mobs_names)
        print(dict(basket))
        print(player.income, player.money, player.power)


TEST_END = '\n\n\n'


def _test_quick_money_planner(necessary_money):
    start_time = get_current_time()
    tactic = get_tactic_by_necessary_money(necessary_money)
    execution_time = get_current_time() - start_time
    print("Execution time:", execution_time)
    print("Result:")
    print_tactic(tactic)
    print(end=TEST_END)


def test_quick_money_planner():
    necessary_money = int(input("Find the quickest way to reach money: "))
    _test_quick_money_planner(necessary_money)


def _test_max_income_planner(wave_count):
    start_time = get_current_time()
    tactic_generator = get_max_income_tactic()
    tactic = [next(tactic_generator) for _ in range(wave_count)]
    execution_time = get_current_time() - start_time
    print("Execution time:", execution_time)
    print("Result:")
    print_tactic(tactic)
    print(TEST_END)


def test_max_income_planner():
    waves = int(input("Find max-income tactic for waves forward: "))
    _test_max_income_planner(waves)


def _test_forker(func, _func, player, options):
    func_name = func.__name__
    print("Name:", func_name)

    start_time = get_current_time()
    result = func(player)
    execution_time = get_current_time() - start_time
    print("Execution time:", execution_time)

    cache_info = _func.cache_info()
    print("Cache info:", cache_info)

    if options["do_second_test"]:
        player.money -= 1
        player.power -= 1

        start_time = get_current_time()
        result_2 = func(player)
        execution_time_2 = get_current_time() - start_time
        print("Second execution time:", execution_time_2)

        cache_info_2 = _func.cache_info()
        print("Second cache info:", cache_info_2)

    _func.cache_clear()

    result_length = len(result)
    print("Result length:", result_length)

    if options["do_result_repeating_test"]:
        def sort_basket(basket):
            return tuple(sorted(basket, key=lambda kind: kind.name))

        result = set(map(sort_basket, result))
        real_result_length = len(result)

        if result_length == real_result_length:
            print("No basket repeating.")
        else:
            print("There is basket repeating. Real length is %s." % real_result_length)

    print(TEST_END)


def test_forker():
    player = Player()
    player.money = 1000000000
    player.add_time(25*25)
    player.do_limit_mob_stock = False
    player.add_time(25)
    _func = NoMoneyAlgorithm._compute_available_baskets.__func__
    options = {
        "do_second_test": 0,
        "do_result_repeating_test": 0
    }
    return _test_forker(compute_available_baskets, _func, player, options)


tests = {
    test_quick_money_planner: 0,
    test_max_income_planner: 0,
    test_forker: 1
}


if __name__ == "__main__":
    for test, do_test in tests.items():
        if do_test:
            test()
