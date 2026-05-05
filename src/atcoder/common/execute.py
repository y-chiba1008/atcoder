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


def display_case_result(
    case_name: str,
    result: bool,
    stdin: str,
    stdout: str,
    expected: str,
) -> None:
    """
    個別のテストケースの実行結果をコンソールに色付きで表示する
    """
    # ケース名と合否 (AC/WA) の表示
    click.secho(f'▶ case {case_name} ', fg='cyan', bold=True, nl=False)
    if result:
        click.secho('[AC]', fg='green', bold=True)
    else:
        click.secho('[WA]', fg='red', bold=True)

    # 標準入力の表示
    click.secho('  stdin:', fg='blue')
    click.echo(f'    {stdin.replace("\n", "\n    ")}')

    # 標準出力の表示
    click.secho('  stdout:', fg='blue')
    click.echo(f'    {stdout.strip().replace("\n", "\n    ")}')

    # 不正解時のみ期待される出力を表示
    if not result:
        click.secho('  expected:', fg='yellow')
        click.echo(f'    {expected.replace("\n", "\n    ")}')

    click.echo('-' * 40)


def display_execution_summary(passed_count: int, total_count: int) -> None:
    """
    全ケース実行後の最終的な統計情報を表示する
    """
    click.echo()
    summary_color = 'green' if passed_count == total_count else 'red'
    click.secho(
        f'Summary: {passed_count}/{total_count} cases passed.',
        fg=summary_color,
        bold=True,
    )


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
    help='ケース番号 カンマ区切りで複数指定可能, 省略の場合、全ケースを実行する',
)
def run(contest: str, task: str, heuristics: bool, case: str | None) -> None:
    """
    指定したコンテスト・タスクのプログラムを実行し、テストデータと照合する
    """
    # 実行対象となる問題の main 関数を動的に読み込む
    module_name = f'atcoder.contests.{contest}.{task}_main'
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        click.secho(f'Error: Module {module_name} not found. ({e})', fg='red', err=True)
        return

    main_func = getattr(module, 'main', None)
    if not main_func:
        click.secho(
            f'Error: "main" function not found in {module_name}', fg='red', err=True
        )
        return

    # 実行ディレクトリからテスト対象となるケースファイルを特定する
    contest_dir = pathlib.Path(__file__).parent.parent / 'contests' / contest
    if not contest_dir.exists():
        click.secho(
            f'Error: Contest directory {contest_dir} not found.', fg='red', err=True
        )
        return

    case_numbers = [int(x.strip()) for x in case.split(',')] if case else None

    test_files = sorted(contest_dir.glob(f'{task}_case_*.txt'))
    if case_numbers:
        test_files = [
            f for f in test_files if int(f.stem.split('_')[-1]) in case_numbers
        ]

    if not test_files:
        click.secho(
            f'No test cases found for {task} in {contest}', fg='yellow', err=True
        )
        return

    passed_count = 0
    total_count = len(test_files)

    # 各テストケースに対してプログラムを実行し、結果を照合・表示する
    for test_file in test_files:
        case_name = test_file.stem
        stdin_content, expected_output = parse_test_case(test_file)

        dummy_io = DummyIO(stdin_content)

        # ターゲットの main 関数を DummyIO 経由で呼び出す
        try:
            main_func(input=dummy_io.input, print=dummy_io.print)
        except Exception as e:
            click.secho(f'Error executing {case_name}: {e}', fg='red', err=True)
            continue

        actual_output = dummy_io.stdout.strip()
        expected_output = expected_output.strip()
        result = actual_output == expected_output

        if result:
            passed_count += 1

        # 結果の出力処理を外部関数に委譲
        display_case_result(
            case_name=case_name,
            result=result,
            stdin=stdin_content,
            stdout=dummy_io.stdout,
            expected=expected_output,
        )

    # 全ケースの実行完了後、サマリーを表示
    display_execution_summary(passed_count=passed_count, total_count=total_count)


if __name__ == '__main__':
    cli()
