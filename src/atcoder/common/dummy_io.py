from dataclasses import dataclass, field
from typing import Generator


@dataclass
class DummyIO:
    stdin: str
    stdout: str = field(default='', init=False)
    _input_gen: Generator[str, None, None] = field(init=False)

    def __post_init__(self):
        self._input_gen = (row for row in self.stdin.split('\n'))

    def input(self) -> str:
        try:
            return next(self._input_gen)
        except StopIteration:
            return ''

    def print(self, *values: object, sep=' ', end='\n'):
        values_str = sep.join([str(v) for v in values]) + end
        self.stdout += values_str
