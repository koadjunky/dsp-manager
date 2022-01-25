import pytest

from dsp_be.logic.config import Config
from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet
from dsp_be.logic.stack import Stack


@pytest.fixture
def jupiter():
    return Planet(
        name="Earth",
        resources={"fire_ice": 0.04, "hydrogen": 0.85},
        exports=[],
        imports=[],
        star=None,
    )


@pytest.fixture
def veins_utilization_two():
    return Config(veins_utilization=2)


@pytest.fixture
def orbital_collector(jupiter, veins_utilization_two):
    return Factory(
        name="Collector #1",
        machine_name="orbital_collector",
        recipe_name="orbital_collector",
        count=40,
        planet=jupiter,
        config=veins_utilization_two,
    )


def test_orbital_collector(jupiter, orbital_collector):
    print(jupiter.production())
    assert jupiter.production() == Stack(
        products={
            "deuterium": 0.0,
            "hydrogen": pytest.approx(196.4, 0.01),
            "fire_ice": pytest.approx(9.24, 0.01),
        }
    )


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main(["-vv"]))
