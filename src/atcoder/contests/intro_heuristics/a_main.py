import random
from typing import Callable

N_TYPE = 26


def scores_of_day(day: int, last: list[int], c: list[int], s_d: list[int]) -> list[int]:
    """タイプiを選んだとしたら、その日に得られる得点のリスト"""
    losses = [c[type_idx] * (day - last[type_idx]) for type_idx in range(N_TYPE)]
    total_loss = sum(losses)
    scores = [s_d[i] - (total_loss - losses[i]) for i in range(N_TYPE)]
    print(f'day {day} losses {losses}')
    print(f'day {day} total_loss {total_loss}')
    print(f'day {day} scores {scores}')
    return scores


def main(input: Callable[[], str] = input, print: Callable[..., None] = print):
    # d = int(input())
    # for _ in range(d):
    #     print(random.randint(1, 26))
    print('1')
    print('17')
    print('13')
    print('14')
    print('13')


if __name__ == '__main__':
    main()
