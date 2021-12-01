"""
test_support.py
"""
from pyconcurrent.support import Timer, create_id_lists


def test_timer():
    with Timer() as t:
        [i for i in range(5_000)]

    assert t.start > 0
    assert t.end > 0
    assert t.elapsed_time > 0


def test_create_id_lists():
    actual_lists = create_id_lists(5000, 5)
    assert len(actual_lists) == 5
    assert actual_lists[0] == list(range(1, 1001))
    assert actual_lists[1] == list(range(1001, 2001))
    assert actual_lists[2] == list(range(2001, 3001))
    assert actual_lists[3] == list(range(3001, 4001))
    assert actual_lists[4] == list(range(4001, 5001))

    actual_lists = create_id_lists(5000, 6)
    assert len(actual_lists) == 7
    assert actual_lists[0] == list(range(1, 834))
    assert actual_lists[1] == list(range(834, 1667))
    assert actual_lists[2] == list(range(1667, 2500))
    assert actual_lists[3] == list(range(2500, 3333))
    assert actual_lists[4] == list(range(3333, 4166))
    assert actual_lists[5] == list(range(4166, 4999))
    assert actual_lists[6] == list(range(4999, 5001))

