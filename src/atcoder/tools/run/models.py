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
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise RuntimeError(f'Module {module_name} not found.')

    main_func = getattr(module, 'main', None)
    if not main_func:
        raise RuntimeError(f'"main" function not found in {module_name}')

    return main_func


def load_score_functions(
    contest: str, task: str
) -> tuple[Callable[[int], str], Callable[[str, str], int | float]]:
    """
    指定したコンテストとタスクのスコア計算用関数を動的に読み込む。

    Args:
        contest (str): コンテスト名
        task (str): タスク名

    Returns:
        tuple: (generate_case, calc_score) のタプル

    Raises:
        RuntimeError: モジュールまたは関数が見つからない場合
    """
    module_name = f'atcoder.contests.{contest}.{task}_score'
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise RuntimeError(f'Score module {module_name} not found.')

    generate_case = getattr(module, 'generate_case', None)
    calc_score = getattr(module, 'calc_score', None)

    if not generate_case or not calc_score:
        raise RuntimeError(
            f'Required score functions (generate_case, calc_score) not found in {module_name}'
        )

    return generate_case, calc_score


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
    マーカーがない場合はファイル全体を入力と見なす。

    Args:
        file_path (pathlib.Path): テストケースファイルのパス

    Returns:
        tuple[str, str]: (標準入力の内容, 期待される出力の内容)
    """
    content = file_path.read_text(encoding='utf-8')
    lines = content.splitlines()

    input_lines: list[str] = []
    output_lines: list[str] = []

    current_target = None
    has_marker = False

    for line in lines:
        normalized_line = line.strip().lower()
        if normalized_line == '==== input ====':
            current_target = input_lines
            has_marker = True
            continue
        elif normalized_line == '==== output ====':
            current_target = output_lines
            has_marker = True
            continue

        if current_target is not None:
            current_target.append(line)

    if not has_marker:
        return content.strip(), ''

    return '\n'.join(input_lines).strip(), '\n'.join(output_lines).strip()
