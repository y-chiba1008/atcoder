import click

from atcoder.tools.run.controller import heuristics, run


@click.group()
def cli() -> None:
    """AtCoder 開発補助ツールのエントリポイント。"""
    pass


cli.add_command(run)
cli.add_command(heuristics)


if __name__ == '__main__':
    cli()
