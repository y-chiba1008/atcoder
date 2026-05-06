import io
import random

from atcoder.contests.intro_heuristics.a_main import N_TYPE, scores_of_day


def generate_case(seed: int) -> str:
    """指定されたシードに基づく入力を生成する。"""
    random.seed(seed)

    d = 365
    c = [str(random.randint(0, 100)) for _ in range(N_TYPE)]
    s = [[str(random.randint(0, 20000)) for _ in range(N_TYPE)] for day in range(d)]

    c_str = ' '.join(c)
    s_str = [' '.join(row) for row in s]

    with io.StringIO() as s_buffer:
        print(d, file=s_buffer)
        print(c_str, file=s_buffer)
        for s_row in s_str:
            print(s_row, file=s_buffer)

        return s_buffer.getvalue()


def calc_score(input_str: str, output_str: str) -> int:
    """入出力に基づくスコア計算。"""
    # 入力を変換
    input_rows = input_str.splitlines()[::-1]
    output_rows = output_str.splitlines()[::-1]

    D = int(input_rows.pop())
    c = [int(item) for item in input_rows.pop().split()]
    s: list[list[int]] = []
    for _ in range(D):
        s.append([int(item) for item in input_rows.pop().split()])
    t: list[int] = []
    for _ in range(D):
        t.append(int(output_rows.pop()))

    # タイプ毎の最後に実施した日
    last = [0 for _ in range(N_TYPE)]

    score_total = 0
    for day, s_d, t_d in zip(range(1, D + 1), s, t):
        i = t_d - 1
        scores = scores_of_day(day, last, c, s_d)
        print(f'day {day} choiced score {scores[i]}')
        score_total += scores[i]
        last[i] = day

    return max(10**6 + score_total, 0)
