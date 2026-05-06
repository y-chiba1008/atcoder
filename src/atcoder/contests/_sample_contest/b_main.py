from typing import Callable


def main(input: Callable[[], str] = input, print: Callable[..., None] = print):
    n = int(input())
    print(n)


if __name__ == '__main__':
    main()
