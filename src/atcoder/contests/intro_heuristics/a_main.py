import random
from typing import Callable

N_TYPE = 26


def scores_of_day(day: int, last: list[int], c: list[int], s_d: list[int]) -> list[int]:
    """タイプiを選んだとしたら、その日に得られる得点のリスト"""
    losses = [c[type_idx] * (day - last[type_idx]) for type_idx in range(N_TYPE)]
    total_loss = sum(losses)
    scores = [s_d[i] - (total_loss - losses[i]) for i in range(N_TYPE)]
    return scores


def main(input: Callable[[], str] = input, print: Callable[..., None] = print):
    # 入力
    D = int(input())
    c = [int(item) for item in input().split()]
    s: list[list[int]] = []
    for _ in range(D):
        s.append([int(item) for item in input().split()])

    # タイプ毎の最後に実施した日
    last = [0 for _ in range(N_TYPE)]

    # 貪欲法
    score_total = 0
    for day, s_d in zip(range(1, D + 1), s):
        scores = scores_of_day(day, last, c, s_d)
        max_score = max(scores)
        max_idx = scores.index(max_score)
        print(max_idx + 1)


if __name__ == '__main__':
    main()
