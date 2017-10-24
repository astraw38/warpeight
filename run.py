# warp factor *
# warp *
import os
import re
from collections import Counter

import pytest

NUMBA_DICT = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10}

NUMBAS = '|'.join(NUMBA_DICT.keys())

WARP_RE = re.compile(r'warp (factor )?(?P<speed>\w+\s*(point \w+)?)',
                     re.IGNORECASE)

SEASON_TO_EPIS = [
    (101, 127),
    (127, 149),
    (149, 175),
    (175, 201),
    (201, 227),
    (227, 253),
    (253, 278),
]


def count_warps(filename, season, episode):
    with open(filename, 'r') as f:
        data = f.read()
    matches = WARP_RE.finditer(data)
    speeds = []
    for match in matches:
        try:
            speed = convert_to_decimal(match.groupdict()['speed'])
        except Exception as exc:
            pass
        else:
            speeds.append(speed)

    c = Counter(speeds)
    print("In season %s, episode %s: %s" % (season, episode, c))


def convert_to_decimal(speed):
    if 'point' in speed:
        splitter = 'point'
    else:
        splitter = ' '
    x, _, y = speed.partition(splitter)
    speed = NUMBA_DICT[x.strip()]
    if y:
        speed += NUMBA_DICT[y.strip()] / 10
    return speed


@pytest.mark.parametrize('inval,outval', [('nine point three', 9.3),
                                          ('nine', 9),
                                          ('eight ', 8),
                                          ('ten point eight', 10.8)])
def test_conversion(inval, outval):
    assert convert_to_decimal(inval) == outval


def get_season_and_no(fname):
    epi_number = fname.partition(".")[0]
    for index, season in enumerate(SEASON_TO_EPIS, 1):
        if int(epi_number) in range(season[0], season[1]):
            return index, season[1] - int(epi_number)


if __name__ == "__main__":
    for fname in os.listdir('NextGen'):
        if '.htm' in fname:
            try:
                season, episode = get_season_and_no(fname)
            except Exception:
                print("Failed to find season/episode # for %s" % fname)
                continue
            count_warps(os.path.join('NextGen', fname), season, episode)
