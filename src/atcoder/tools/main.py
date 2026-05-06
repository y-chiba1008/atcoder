import click

from atcoder.tools.run.controller import run


@click.group()
def cli() -> None:
    """AtCoder 開発補助ツールのエントリポイント。"""
    pass


cli.add_command(run)


if __name__ == '__main__':
    cli()
