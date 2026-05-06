import importlib
import pathlib
from typing import Any, Callable


def load_main_func(contest: str, task: str) -> Callable[..., Any]:
    """
    指定したコンテストとタスクの main 関数を動的に読み込む。

    Args:
        contest (str): コンテスト名 (例: 'abc001')
        task (str): タスク名 (例: 'a')

    Returns:
        Callable[..., Any]: 読み込まれた main 関数

    Raises:
        RuntimeError: モジュールまたは main 関数が見つからない場合
    """
    module_name = f'atcoder.contests.{contest}.{task}_main'
    module = importlib.import_module(module_name)

    main_func = getattr(module, 'main', None)
    if not main_func:
        raise RuntimeError(f'"main" function not found in {module_name}')

    return main_func


def get_test_files(contest: str, task: str, case: str | None) -> list[pathlib.Path]:
    """
    実行対象となるテストケースファイルのパスリストを取得する。

    Args:
        contest (str): コンテスト名
        task (str): タスク名
        case (str | None): 指定されたケース番号（カンマ区切り）。None の場合は全ケース。

    Returns:
        list[pathlib.Path]: テストケースファイルの pathlib.Path リスト

    Raises:
        RuntimeError: コンテストディレクトリが見つからない、またはテストケースが存在しない場合
    """
    # src/atcoder/contests ディレクトリへのパスを構築
    # models.py が src/atcoder/tools/run/ にあることを前提としている
    base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
    contest_dir = base_dir / 'contests' / contest

    if not contest_dir.exists():
        raise RuntimeError(f'Contest directory {contest_dir} not found.')

    case_numbers = [int(x.strip()) for x in case.split(',')] if case else None

    test_files = sorted(contest_dir.glob(f'{task}_case_*.txt'))
    if case_numbers:
        test_files = [
            f for f in test_files if int(f.stem.split('_')[-1]) in case_numbers
        ]

    if not test_files:
        raise RuntimeError(f'No test cases found for {task} in {contest}')

    return test_files


def parse_test_case(file_path: pathlib.Path) -> tuple[str, str]:
    """
    テストデータファイルを解析して(input, expected_output)を返す。

    Args:
        file_path (pathlib.Path): テストケースファイルのパス

    Returns:
        tuple[str, str]: (標準入力の内容, 期待される出力の内容)
    """
    lines = file_path.read_text(encoding='utf-8').splitlines()

    input_lines: list[str] = []
    output_lines: list[str] = []

    current_target = None

    for line in lines:
        normalized_line = line.strip().lower()
        if normalized_line == '==== input ====':
            current_target = input_lines
            continue
        elif normalized_line == '==== output ====':
            current_target = output_lines
            continue

        if current_target is not None:
            current_target.append(line)

    return '\n'.join(input_lines).strip(), '\n'.join(output_lines).strip()
