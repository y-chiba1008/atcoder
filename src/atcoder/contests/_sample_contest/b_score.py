import random


def generate_case(seed: int) -> str:
    """指定されたシードに基づく入力を生成する。"""
    random.seed(seed)
    n = random.randint(1, 1000)
    return str(n)


def calc_score(input_str: str, output_str: str) -> int:
    """入出力に基づくスコア計算。"""
    try:
        n = int(output_str)
        return n * 10
    except ValueError:
        return 0
