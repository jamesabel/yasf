
from yasf import sf, sf_separate, structured_sentinel


def test_sf_separate():
    s = sf("user", "person", name="James", id=123)
    print(s)
    assert s == 'user,person ' + structured_sentinel + ' {"name": "James", "id": 123} ' + structured_sentinel
    args, kwargs = sf_separate(s)
    print(f"{args=}")
    print(f"{kwargs=}")
    assert args == "user,person"
    assert kwargs == '{"name": "James", "id": 123}'
