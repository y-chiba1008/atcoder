import click


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


def display_error(e, prefix: str = 'Error'):
    click.secho(f'{prefix}: {e}', fg='red', err=True)
