from typing import Callable

N_TYPE = 26


def score_of_day(
    day: int, last: list[int], c: list[int], s_d: list[int], t_d: int
) -> int:
    i = t_d - 1
    score = s_d[i]
    last[i] = day
    costs = [c[type_idx] * (day - last[type_idx]) for type_idx in range(N_TYPE)]
    score -= sum(costs)
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

    # タイプ毎の最後に実施した日
    last = [0 for _ in range(N_TYPE)]

    score_total = 0
    for day, s_d, t_d in zip(range(1, D + 1), s, t):
        score_total += score_of_day(day, last, c, s_d, t_d)
        print(score_total)


if __name__ == '__main__':
    main()
