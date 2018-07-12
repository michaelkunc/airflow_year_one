import etl

import pytest


@pytest.fixture(scope="session")
def team():
    return etl.get_team(4)


def test_get_team_size(team):
    assert len(team) == 4


def test_get_team_members(team):
    assert all(t in etl.AVENGERS for t in team)
