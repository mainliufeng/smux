# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os

import click

from smux.tmux import Tmux


tmux = Tmux()


@click.command(help='tmux quick switch')
def smux():
    while True:
        click.clear()
        click.echo(tmux.query)
        click.echo(tmux.display(), nl=False)

        c = click.getchar()
        handle_input(c, tmux)


def handle_input(c, tmux):
    if c == '\x1b':  # ESC
        sys.exit(0)
    if c == '\x0d':  # ENTER
        tmux.switch()
        sys.exit(0)
    if c in [
        str(number)[0] for number in range(1, tmux.DISPLAY_COUNT + 1)
    ]:
        index = int('' + c)
        tmux.switch(index)
        sys.exit(0)
    else:
        query = tmux.query
        if c == '\x7f':  # delete
            query = query[:-1]
        else:
            query += c
        tmux.query = query
        tmux.filter()
