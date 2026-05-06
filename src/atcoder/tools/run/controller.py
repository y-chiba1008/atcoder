"""
コンテストの実行とテスト結果の照合を制御するコントローラーモジュール。
"""

import click

from atcoder.common.dummy_io import DummyIO
from atcoder.tools.run.models import get_test_files, load_main_func, parse_test_case
from atcoder.tools.run.views import (
    display_case_result,
    display_error,
    display_execution_summary,
)


@click.command()
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
    指定したコンテスト・タスクのプログラムを実行し、テストデータと照合する。

    Args:
        contest (str): コンテストのキー (例: 'abc001')
        task (str): コンテスト内のタスク (例: 'a')
        heuristics (bool): ヒューリスティック問題の場合は True
        case (str | None): 実行するケース番号 (例: '1,2,3')。省略時は全ケース実行。
    """
    # 実行対象のmain関数を取得
    try:
        main_func = load_main_func(contest, task)
    except RuntimeError as e:
        display_error(e)
        return

    # 実行ディレクトリからテスト対象となるケースファイルを特定する
    try:
        test_files = get_test_files(contest, task, case)
    except RuntimeError as e:
        display_error(e)
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
            display_error(e, prefix=f'Error executing {case_name}')
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
