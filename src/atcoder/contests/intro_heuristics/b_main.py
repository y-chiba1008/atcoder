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
    t: list[int] = []
    for _ in range(D):
        t.append(int(input()))

    score = 0
    days = range(1, D + 1)
    last = [0 for _ in range(N_TYPE)]
    for day, s_d, t_d in zip(days, s, t):
        score += score_of_day(day, c, s_d, t_d, last)
        last[t_d - 1] = day
        print(score)


if __name__ == '__main__':
    main()
