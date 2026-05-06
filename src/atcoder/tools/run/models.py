import importlib
import pathlib


def load_main_func(contest: str, task: str):
    module_name = f'atcoder.contests.{contest}.{task}_main'

    # raise ImportError if not found module
    module = importlib.import_module(module_name)

    main_func = getattr(module, 'main', None)
    if not main_func:
        raise RuntimeError(f'"main" function not found in {module_name}')

    return main_func


def get_test_files(contest, task, case):
    contest_dir = pathlib.Path(__file__).parent.parent.parent / 'contests' / contest
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
    テストデータファイルを解析して(input, expected_output)を返す
    """
    content = file_path.read_text(encoding='utf-8')
    parts = content.split('# expected output')
    if len(parts) != 2:
        parts = content.split('# excepted output')

    input_part = parts[0].replace('# input', '').strip()
    expected_output_part = parts[1].strip() if len(parts) > 1 else ''

    return input_part, expected_output_part
