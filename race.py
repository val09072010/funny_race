import sys
from typing import TypeVar, Optional
from dataclasses import dataclass


UNIT = 'min.'

TTrack = TypeVar("TTrack", bound=list[list])

SMALL: TTrack = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
]

SMALL_P: TTrack = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 1, 1],
    [1, 1, 1, 0],
]

TRACK_SIMPLE: TTrack = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

NARROW_O: TTrack = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
]

OLYMPIC: TTrack = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
]

TRACKS: dict[str, TTrack] = {
    'simple': TRACK_SIMPLE,
    'narrow': NARROW_O,
    'olympic': OLYMPIC,
    'small': SMALL,
    'small_p': SMALL_P
}


def track_factory(track_name: str) -> TTrack:
    recent_track = TRACKS.get(track_name, None)
    if not recent_track:
        recent_track = TRACK_SIMPLE
    return recent_track


@dataclass
class TResult:
    time: int
    schema: str


class DefaultStrategy:
    def calc(self, track: TTrack) -> str:
        raise NotImplemented


class AlwaysOneStrategy(DefaultStrategy):
    """Slowest strategy to baseline result"""
    def calc(self, track: TTrack) -> str:
        track_len = sum([sum(x) for x in track]) - 2
        return '0' + '1' * track_len


class NaiveStrategy(DefaultStrategy):
    """suboptimal attempt to complete the track"""
    @staticmethod
    def run_segment(current_velocity: int, start_x: int, end_x: int, velocity_limit: int, speed_trace: list,
                    dv: int = 1) -> int:
        if end_x == start_x:
            speed_trace.append(current_velocity)
            return current_velocity
        if end_x - start_x < current_velocity or start_x > end_x:
            new_v = current_velocity - dv
            speed_trace.append(new_v)
            return new_v
        if current_velocity + dv <= velocity_limit:
            current_velocity += dv
        return NaiveStrategy.run_segment(current_velocity, start_x + current_velocity, end_x,
                                         velocity_limit, speed_trace)

    def _linearize(self, track: TTrack) -> list:
        def _get(r, c) -> Optional[int]:
            if r < 0 or c < 0:
                return False  # should handle python strength - hide negative index :)
            try:
                return track[r][c]
            except Exception:
                return 0

        res = [1]
        rows = len(track)
        cols = len(track[0])
        cells = rows * cols
        i = 0
        j = 1
        d_i = 0
        d_j = 1
        for _ in range(cells):  # some sort of 'while True' with limits
            if _get(i, j):
                res.append(1)

            if d_j:
                n_j = j + d_j
                if n_j >= cols or n_j < 0 or not _get(i, n_j):
                    res[-1] = -1
                    d_j = 0
                    if _get(i - 1, j):
                        d_i = -1
                    elif _get(i + 1, j):
                        d_i = 1
                    else:
                        print(f'Seems we reached finish earlier? {(i, j)}')
                        break
            elif d_i:
                if i == 2 and j == 3:
                    print(1)
                n_i = i + d_i
                if n_i >= rows or n_i < 0 or not _get(n_i, j):
                    res[-1] = -1
                    d_i = 0
                    if _get(i, j - 1):
                        d_j = -1
                    elif _get(i, j + 1):
                        d_j = 1
                    else:
                        print(f'Seems we reached finish earlier? {(i, j)}')
                        break
            i += d_i
            j += d_j
            if i == 0 and j == 0:
                print(f'We reached finish: {(i, j)}')
                res[0] = 0  # initial velocity should be zero
                break
        return res

    def _velocity_map(self, l_track: list[int]) -> list:
        if not (l_track and isinstance(l_track, list)):
            return []
        change_points = []
        try:
            for i, cell in enumerate(l_track):
                if cell == -1:
                    change_points.append(i)
            res = [0] * len(l_track)
            for i, v in enumerate(change_points[:-1]):
                res[v] = change_points[i + 1] - change_points[i]
            res[change_points[-1]] = len(l_track) - change_points[-1] - 1
            res[-2:] = [2, 1]
            return res
        except Exception:
            return []

    def calc(self, track: TTrack) -> str:
        l_track = self._linearize(track)
        speed_map = self._velocity_map(l_track)
        schema = [0, 1]

        c_i = 1
        c_v = 1
        ids = []

        for i, c in enumerate(speed_map):
            if c:
                ids.append((i, c))

        for i, v in ids:
            while c_i != i:
                new_v = NaiveStrategy.run_segment(c_v, c_i, i, v, schema)
                c_i += new_v
                c_v = new_v
        return ''.join(map(str, schema))


TStrategy = TypeVar("TStrategy", bound=DefaultStrategy)


class TRacer:
    __slots__ = ['name', 'strategy', 'track_path']

    def __init__(self, name: str, strategy: TStrategy):
        self.name = name
        self.strategy = strategy
        self.track_path = None

    def set_strategy(self, new_strategy: callable):
        if not new_strategy:
            print(f'New strategy must not be None or empty object')
            return
        self.strategy = new_strategy

    def _print_track(self, track: TTrack, label: str = 'INIT'):
        print(f'____________ {label} _______________')
        for track_line in track:
            print('  '.join(list(map(str, track_line))))
        print('__________________________________')

    def _validate_track(self, track: TTrack) -> bool:
        if not track:
            return False
        try:
            res = sum([sum(x) for x in track])  # TODO: add check for topology of track
            return bool(res)
        except Exception:
            return False

    def run(self, track: TTrack) -> Optional[TResult]:
        if not self._validate_track(track):
            print(f'Track {track} is invalid. It must be list of lists of 0 and 1')
            return None
        self._print_track(track)
        res = self.strategy.calc(track)
        track_time = len(res) + 1
        return TResult(track_time, res)


def max_velocity(current_velocity: int, start_x: int, end_x: int, velocity_limit: int, dv: int = 1) -> int:
    # method for testing Naive strategy
    if end_x == start_x or current_velocity + dv > velocity_limit:
        return current_velocity
    if end_x - start_x < current_velocity or start_x > end_x:
        return current_velocity - dv
    if current_velocity + dv <= velocity_limit:
        current_velocity += dv
    return max_velocity(current_velocity, start_x + current_velocity, end_x, velocity_limit)


def racer_factory(strategy: TStrategy = None, name=None):
    return TRacer(name=name if name else 'Dummy', strategy=strategy if strategy else AlwaysOneStrategy())


def main(args):
    if not args:
        print(f'USAGE: python {__file__} <track_name>.\nAvailable tracks are: {list(TRACKS.keys())}')
        sys.exit(0)
    track_name = str(args[0]).lower()
    if track_name not in TRACKS:
        print(f'Unknown Track name <{args[0]}>, please use one of the available: {list(TRACKS.keys())}')
        sys.exit(-1)

    track = track_factory(track_name)
    racer = racer_factory(NaiveStrategy())
    res: TResult = racer.run(track)

    if not res:
        print(f"An error occurs during race can't complete calculations")
        return
    print(f"Racer '{racer.name}' completed the track '{track_name}' in {res.time} {UNIT} with path {res.schema}")


if __name__ == '__main__':
    main(sys.argv[1:])
