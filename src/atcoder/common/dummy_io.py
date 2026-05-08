import io
from dataclasses import dataclass, field
from typing import Any, Generator


@dataclass
class DummyIO:
    """
    競技プログラミングのプログラムを実行する際に、標準入出力をシミュレートするためのクラス。
    """

    stdin: str
    _stdout_buffer: io.StringIO = field(
        default_factory=io.StringIO, init=False, repr=False
    )
    _input_gen: Generator[str, None, None] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # 入力文字列を改行で分割し、ジェネレータを作成
        self._input_gen = (line for line in self.stdin.splitlines())

    def input(self) -> str:
        """
        標準入力から1行読み込む。Python標準の input() の動作をシミュレートする。

        Returns:
            str: 読み込んだ文字列

        Raises:
            EOFError: 入力がこれ以上ない場合
        """
        try:
            return next(self._input_gen)
        except StopIteration:
            raise EOFError('EOF when reading a line')

    def print(self, *values: Any, sep: str = ' ', end: str = '\n') -> None:
        """
        標準出力に書き込む。Python標準の print() の動作をシミュレートする。

        Args:
            *values (Any): 出力する値
            sep (str): 値の区切り文字
            end (str): 行末の文字
        """
        print(*values, sep=sep, end=end, file=self._stdout_buffer)

    def close(self) -> None:
        """内部バッファを閉じる。"""
        self._stdout_buffer.close()

    def __enter__(self) -> 'DummyIO':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    @property
    def stdout(self) -> str:
        """
        これまでに蓄積された標準出力の内容を文字列として取得する。

        Returns:
            str: 蓄積された出力内容
        """
        return self._stdout_buffer.getvalue()
