from abc import ABCMeta, abstractmethod

from mobwars.data import load_data


_mob_fields = (
    "name",
    "power_cost",
    "money_cost",
    "cooldown",  # TODO: rename param to sth
    "income",
    "hp",
    "unlock_time",
    "stack_size"
    # todo "damage"
    # todo "defense"
    # todo "speed"
    # todo other
)


@abstractmethod
def mob_attribute():
    raise TypeError("mob_attribute is not callable")


Mob = ABCMeta(
    "Mob",
    (),
    {field: mob_attribute for field in _mob_fields}
)


def make_mob_class(mob_data):
    kind = type("Mob", (Mob,), mob_data)
    return kind


mob_kinds = map(make_mob_class, load_data()["mobs"])
mob_kinds = tuple(mob_kinds)

# TODO: rename mob to mob_kind everywhere
