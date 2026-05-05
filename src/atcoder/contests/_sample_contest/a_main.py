from typing import Callable


def main(input: Callable[[], str] = input, print: Callable[..., None] = print):
    while True:
        row = input()
        if row == '':
            break
        print(row)


if __name__ == '__main__':
    main()
