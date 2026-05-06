"""
コンテストの実行とテスト結果の照合を制御するコントローラーモジュール。
"""

from typing import Any, Callable

import click

from atcoder.common.dummy_io import DummyIO
from atcoder.tools.run.models import (
    get_test_files,
    load_main_func,
    load_score_functions,
    parse_test_case,
)
from atcoder.tools.run.views import (
    display_case_result,
    display_error,
    display_execution_summary,
    display_heuristics_case_result,
    display_heuristics_summary,
)


def _execute_main(
    main_func: Callable[..., Any], stdin_content: str, case_name: str
) -> str | None:
    """main関数を実行し、標準出力を返す。エラー時はNoneを返す。"""
    with DummyIO(stdin_content) as dummy_io:
        try:
            main_func(input=dummy_io.input, print=dummy_io.print)
            return dummy_io.stdout.strip()
        except EOFError:
            display_error(
                'Unexpected EOF (The program tried to read more input than available)',
                prefix=f'Error executing {case_name}',
            )
        except Exception as e:
            display_error(e, prefix=f'Error executing {case_name}')
    return None


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
    """
    # 実行対象のmain関数を取得
    try:
        main_func = load_main_func(contest, task)
    except RuntimeError as e:
        display_error(e)
        return

    if heuristics:
        # ヒューリスティックモードの実行
        try:
            generate_case, calc_score = load_score_functions(contest, task)
        except RuntimeError as e:
            display_error(e)
            return

        scores = []

        if case:
            # ケース指定がある場合はファイルから実行
            try:
                test_files = get_test_files(contest, task, case)
            except RuntimeError as e:
                display_error(e)
                return

            for test_file in test_files:
                case_name = test_file.stem
                stdin_content, _ = parse_test_case(test_file)
                stdout = _execute_main(main_func, stdin_content, case_name)
                if stdout is not None:
                    score = calc_score(stdin_content, stdout)
                    scores.append(score)
                    display_heuristics_case_result(case_name, stdout, score)
        else:
            # ケース指定がない場合は 0-99 のシードで自動生成
            for seed in range(100):
                case_name = f'seed_{seed:03}'
                stdin_content = generate_case(seed)
                stdout = _execute_main(main_func, stdin_content, case_name)
                if stdout is not None:
                    score = calc_score(stdin_content, stdout)
                    scores.append(score)
                    display_heuristics_case_result(case_name, stdout, score)

        display_heuristics_summary(scores)

    else:
        # 通常モードの実行
        try:
            test_files = get_test_files(contest, task, case)
        except RuntimeError as e:
            display_error(e)
            return

        passed_count = 0
        total_count = len(test_files)

        for test_file in test_files:
            case_name = test_file.stem
            stdin_content, expected_output = parse_test_case(test_file)
            stdout = _execute_main(main_func, stdin_content, case_name)

            if stdout is not None:
                result = stdout == expected_output
                if result:
                    passed_count += 1

                display_case_result(
                    case_name=case_name,
                    result=result,
                    stdin=stdin_content,
                    stdout=stdout,
                    expected=expected_output,
                )

        display_execution_summary(passed_count=passed_count, total_count=total_count)
