import pytest
from race import track_factory, max_velocity, NaiveStrategy


# yes I know - it should converted to fixtures and be moved into con
l_small = [0, 1, 1, -1, 1, -1, 1, 1, -1, 1]
l_simple = [0, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1]
l_narrow = [0, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1]
l_small_p = [0, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1]
l_olympic = [0, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1]
strategy = NaiveStrategy()


@pytest.mark.parametrize('name, exp', [
    ('small', l_small),
    ('simple', l_simple),
    ('narrow', l_narrow),
    ('small_p', l_small_p),
    ('olympic', l_olympic)
])
def test_linearization(name, exp):
    track = track_factory(name)
    assert track
    lin = strategy._linearize(track)
    assert lin
    assert lin == exp


@pytest.mark.parametrize('l_track, exp', [
    (l_small, [0, 0, 0, 2, 0, 3, 0, 0, 2, 1]),
    (l_small_p, [0, 0, 0, 2, 0, 1, 1, 2, 0, 2, 2, 1]),
    (l_simple, [0, 0, 0, 0, 0, 0, 3, 0, 0, 6, 0, 0, 0, 0, 0, 2, 2, 1]),
    (l_olympic, [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 3, 0, 0, 7, 0, 0, 0, 0, 0, 2, 1])
])
def test_velocity_map(l_track, exp):
    v_map = strategy._velocity_map(l_track)
    assert v_map == exp


@pytest.mark.parametrize('param, res', [
    ((1, 1, 7, 4), 2),
    ((2, 7, 11, 4), 2),
    ((1, 1, 6, 3), 3),
    ((2, 5, 8, 2), 2)
])
def test_max_velocity(param, res):
    r = max_velocity(*param)
    assert r == res


def test_speed_tracking():
    # based on small track with velocity map = [0, 0, 0, 2, 0, 3, 0, 0, 2, 1]
    schema = [0, 1]
    r_1 = NaiveStrategy.run_segment(1, 1, 3, 2, schema)
    r_2 = NaiveStrategy.run_segment(r_1, 3, 5, 3, schema)
    r_3 = NaiveStrategy.run_segment(r_2, 5, 8, 2, schema)
    r_4 = NaiveStrategy.run_segment(r_3, 8, 9, 1, schema)
    assert schema == [0, 1, 2, 2, 1, 1]
