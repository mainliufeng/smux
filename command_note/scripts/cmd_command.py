# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os

import click

from command_note.command_table import CommandTable, CommandNote
from command_note.scripts.cmd_help import help_text


LIST_MODE = 'list mode'
HELP_MODE = 'help mode'
SEARCH_MODE = 'search mode'
DELETE_MODE = 'delete mode'
ADD_MODE = 'add mode'
EDIT_MODE = 'edit mode'


@click.command(help='note of command')
def cmd():
    command_table = CommandTable()

    mode = LIST_MODE
    while True:
        if mode == HELP_MODE:
            click.clear()
            click.secho('help mode', bold=True)
            click.echo(help_text)
        elif mode in [LIST_MODE, DELETE_MODE, EDIT_MODE]:
            click.clear()
            echo_mode_page(mode, command_table, with_query=True)
            click.echo(command_table.get_cmd_table())
        elif mode == SEARCH_MODE:
            click.clear()
            echo_mode_page(mode, command_table)
            click.echo(command_table.get_cmd_table())
            click.echo(command_table.get_query(), nl=False)
        elif mode == ADD_MODE:
            mode = add_mode(command_table)
            continue

        c = click.getchar()

        if mode == HELP_MODE:
            ret_mode = help_mode(c, command_table)
        elif mode == LIST_MODE:
            ret_mode = list_mode(c, command_table)
        elif mode == SEARCH_MODE:
            ret_mode = search_mode(c, command_table)
        elif mode == DELETE_MODE:
            ret_mode = delete_mode(c, command_table)
        elif mode == EDIT_MODE:
            ret_mode = edit_mode(c, command_table)

        if ret_mode is not None:
            mode = ret_mode


def echo_mode_page(mode, command_table, with_query=False):
    query = command_table.get_query()
    if with_query and query:
        click.secho(
            '{}\tquery:{}\t{}/{} page'.format(
                mode,
                query,
                *command_table.get_page_info()
            ),
            bold=True
        )
    else:
        click.secho(
            '{}\t{}/{} page'.format(mode, *command_table.get_page_info()),
            bold=True
        )


def add_mode(command_table):
    cmd_note = _get_cmd_note()
    if cmd_note is not None:
        command_table.add_cmd_note(cmd_note)
    return LIST_MODE


def _get_cmd_note(cmd_note=None):
    remove_comment = lambda text: '\n'.join([
        line.strip()
        for line in text.split('\n')
        if line.strip() and not line.strip().startswith('#')
    ])

    cmd = click.edit('# Input command'
                     if cmd_note is None
                     else '# Edit command\n{}'.format(cmd_note.cmd))
    if cmd is None:
        return

    cmd = remove_comment(cmd)
    if not cmd:
        return

    note = click.edit('# Input note'
                      if cmd_note is None
                      else '# Edit note\n{}'.format(cmd_note.note))
    if note is None:
        return

    note = remove_comment(note)
    if not note:
        return

    return CommandNote(cmd, note)


def edit_mode(c, command_table):
    if c == '\x1b':  # ESC
        return LIST_MODE
    elif c == 'n':
        command_table.next_page()
    elif c == 'p':
        command_table.previous_page()
    else:
        index = None
        try:
            index = int(c)
        except ValueError:
            pass

        cmd_note = command_table.get_cmd_note(index)
        if cmd_note is None:
            return LIST_MODE

        cmd_note = _get_cmd_note(cmd_note)
        if cmd_note is not None:
            command_table.edit_cmd_note(index, cmd_note)
        return LIST_MODE


def delete_mode(c, command_table):
    if c == '\x1b':  # ESC
        return LIST_MODE
    elif c == 'n':
        command_table.next_page()
    elif c == 'p':
        command_table.previous_page()
    else:
        index = None
        try:
            index = int(c)
        except ValueError:
            pass

        cmd_note = command_table.get_cmd_note(index)
        if cmd_note is None:
            return LIST_MODE

        if click.confirm(
            'Delete {}: {} ?'.format(cmd_note.note, cmd_note.cmd)
        ):
            command_table.delete_cmd_note(index)
        return LIST_MODE


def search_mode(c, command_table):
    if c == '\x1b':  # ESC
        return LIST_MODE
    else:
        query = command_table.get_query()
        if c == '\x7f':  # delete
            query = query[:-1]
        else:
            query += c
        command_table.set_query(query)


def help_mode(c, command_table):
    if c in ['h', '?', '\x1b']:
        return LIST_MODE


def list_mode(c, command_table):
    if c == 'q':
        sys.exit(0)
    elif c == 's':
        return SEARCH_MODE
    elif c in ['?', 'h']:
        return HELP_MODE
    elif c == 'd':
        return DELETE_MODE
    elif c == 'a':
        return ADD_MODE
    elif c == 'e':
        return EDIT_MODE
    elif c == 'n':
        command_table.next_page()
    elif c == 'p':
        command_table.previous_page()
    else:
        index = None
        try:
            index = int(c)
        except ValueError:
            pass

        if index is not None:
            cmd = command_table.get_cmd(index)
            if cmd is not None:
                click.echo(cmd)
                sys.exit(os.system(cmd))
