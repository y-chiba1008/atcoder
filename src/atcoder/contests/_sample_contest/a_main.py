from typing import Callable


def main(input: Callable[[], str] = input, print: Callable[..., None] = print):
    row = input()
    print(row)


if __name__ == '__main__':
    main()
