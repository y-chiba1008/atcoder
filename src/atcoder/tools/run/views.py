import click


def truncate_text(text: str, max_lines: int = 20) -> str:
    """
    テキストが長い場合に中略して返す。

    Args:
        text (str): 対象のテキスト
        max_lines (int): 表示する最大行数

    Returns:
        str: 処理後のテキスト
    """
    lines = text.strip().splitlines()
    if len(lines) <= max_lines:
        return text.strip()

    half = max_lines // 2
    return '\n'.join(lines[:half] + ['    ... (truncated) ...'] + lines[-half:])


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
    click.echo(f'    {truncate_text(stdin).replace("\n", "\n    ")}')

    # 標準出力の表示
    click.secho('  stdout:', fg='blue')
    click.echo(f'    {truncate_text(stdout).replace("\n", "\n    ")}')

    # 不正解時のみ期待される出力を表示
    if not result:
        click.secho('  expected:', fg='yellow')
        click.echo(f'    {truncate_text(expected).replace("\n", "\n    ")}')

    click.echo('-' * 40)


def display_heuristics_case_result(
    case_name: str,
    stdout: str,
    score: int | float,
) -> None:
    """
    ヒューリスティックモードでの個別結果をコンソールに表示する。
    """
    click.secho(f'▶ case {case_name} ', fg='cyan', bold=True, nl=False)
    click.secho(f'Score: {score}', fg='green', bold=True)

    # 標準出力の表示
    click.secho('  stdout:', fg='blue')
    click.echo(f'    {truncate_text(stdout).replace("\n", "\n    ")}')

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


def display_heuristics_summary(scores: list[int | float]) -> None:
    """
    ヒューリスティックモード実行後の統計情報を表示する。
    """
    if not scores:
        return

    total = len(scores)
    max_score = max(scores)
    min_score = min(scores)
    total_score = sum(scores)

    click.echo()
    click.secho('=== Heuristics Summary ===', fg='magenta', bold=True)
    click.echo(f'Total cases: {total}')
    click.echo(f'Max score:   {max_score}')
    click.echo(f'Min score:   {min_score}')
    click.echo(f'Total score:     {total_score:.2f}')


def display_error(e: Exception | str, prefix: str = 'Error') -> None:
    """
    エラーメッセージを標準エラー出力に赤色で表示する。

    Args:
        e (Exception | str): 表示するエラー内容
        prefix (str): メッセージの接頭辞
    """
    click.secho(f'{prefix}: {e}', fg='red', err=True)
