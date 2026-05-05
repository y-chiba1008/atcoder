import importlib
import pathlib

import click

from atcoder.common.dummy_io import DummyIO


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


@click.group()
def cli():
    """AtCoder 開発補助ツール"""
    pass


@cli.command()
@click.option('--contest', '-c', type=str, required=True, help='コンテストのキー')
@click.option('--task', '-t', type=str, required=True, help='コンテスト内のタスク')
@click.option(
    '--heuristics', '-h', is_flag=True, default=False, help='heuristics問題の場合True'
)
@click.option(
    '--case',
    '-C',
    type=str,
    default=None,
    help='ケース番号 カンマ区切りで複数指定化, 省略の場合、全部',
)
def run(contest: str, task: str, heuristics: bool, case: str | None) -> None:
    """
    指定したコンテスト・タスクのプログラムを実行し、テストデータと照合する
    """
    # モジュールの動的インポート
    module_name = f'atcoder.contests.{contest}.{task}_main'
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        click.echo(f'Error: Module {module_name} not found. ({e})', err=True)
        return

    main_func = getattr(module, 'main', None)
    if not main_func:
        click.echo(f'Error: "main" function not found in {module_name}', err=True)
        return

    # テストデータの特定
    contest_dir = pathlib.Path(__file__).parent.parent / 'contests' / contest
    if not contest_dir.exists():
        click.echo(f'Error: Contest directory {contest_dir} not found.', err=True)
        return

    case_numbers = [int(x.strip()) for x in case.split(',')] if case else None

    test_files = sorted(contest_dir.glob(f'{task}_case_*.txt'))
    if case_numbers:
        test_files = [
            f for f in test_files if int(f.stem.split('_')[-1]) in case_numbers
        ]

    if not test_files:
        click.echo(f'No test cases found for {task} in {contest}', err=True)
        return

    # 実行と結果表示
    for test_file in test_files:
        case_name = test_file.stem
        stdin_content, expected_output = parse_test_case(test_file)

        dummy_io = DummyIO(stdin_content)

        # main関数の引数に合わせて呼び出す
        # 通常は input=..., print=... を受け取る想定
        try:
            main_func(input=dummy_io.input, print=dummy_io.print)
        except Exception as e:
            click.echo(f'Error executing {case_name}: {e}', err=True)
            continue

        actual_output = dummy_io.stdout.strip()
        expected_output = expected_output.strip()
        result = actual_output == expected_output

        click.echo(f'case {case_name} =============')
        click.echo('stdin --------------')
        click.echo(stdin_content)
        click.echo('stdout --------------')
        click.echo(dummy_io.stdout, nl=False)
        click.echo('expected --------------')
        click.echo(expected_output)
        click.echo(f'result: {result}')
        click.echo()


if __name__ == '__main__':
    cli()
