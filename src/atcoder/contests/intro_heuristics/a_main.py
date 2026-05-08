from typing import Callable

N_TYPE = 26


def score_of_day(day, c, s_d, t_d, last):
    gain = s_d[t_d - 1]
    scores = [-cost * (day - last_day) for cost, last_day in zip(c, last)]
    scores[t_d - 1] = gain
    score = sum(scores)
    return score


def main(input: Callable[[], str] = input, print: Callable[..., None] = print):
    # 入力
    D = int(input())
    c = [int(item) for item in input().split()]
    s: list[list[int]] = []
    for _ in range(D):
        s.append([int(item) for item in input().split()])

    days = range(1, D + 1)
    last = [0 for _ in range(N_TYPE)]
    for day, s_d in zip(days, s):
        scores = [
            score_of_day(day, c, s_d, type_temp, last)
            for type_temp in range(1, N_TYPE + 1)
        ]
        max_score = max(scores)
        max_idx = scores.index(max_score)
        print(max_idx + 1)


if __name__ == '__main__':
    main()
