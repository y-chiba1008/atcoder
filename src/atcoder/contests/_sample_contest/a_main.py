from typing import Callable


def main(input: Callable[[], str] = input, print: Callable[..., None] = print):
    print(input())
    print(input())
    print(input())


if __name__ == '__main__':
    main()
