# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import subprocess

from prettytable import PrettyTable
from fuzzywuzzy import process


def load_tmux_windows():
    windows = []
    windows_output = subprocess.check_output(
        [
            'tmux',
            'list-windows',
            '-a',
            '-F',
            '"#{session_name}/#{window_name}"'
        ]
    )
    for window in windows_output.split('\n'):
        if not window:
            continue
        window = window[1:-1]
        session_name = window.split('/')[0]
        window_name = window.split('/')[1]
        windows.append(TmuxWindow(session_name, window_name))
    return windows


def filter_tmux_windows(query, windows, threshold=50):  # max score 100
    if not query:
        return windows
    else:
        search_key_list = []
        search_key_window_dict = {}
        for window in windows:
            search_key = u'{}/{}'.format(
                window.session_name,
                window.window_name
            )
            search_key_list.append(search_key)
            search_key_window_dict[search_key] = window

        search_key_score_list = process.extract(
            query,
            search_key_list,
            limit=len(search_key_list)
        )
        filter_windows = [
            search_key_window_dict[search_key_score[0]]
            for search_key_score in search_key_score_list
            if search_key_score[1] >= threshold
        ]
        return filter_windows


class Tmux(object):

    DISPLAY_COUNT = 50

    def __init__(self):
        self.tmux_windows = load_tmux_windows()
        self.filter_windows = self.tmux_windows[:self.DISPLAY_COUNT]
        self.query = ''

    def filter(self):
        self.filter_windows = filter_tmux_windows(
            self.query,
            self.tmux_windows
        )[:self.DISPLAY_COUNT]

    def switch(self, index=1):
        index = index - 1
        window = self.filter_windows[index]
        # remove '...', example: 'zsh...' window name is 'zsh'
        window_name = window.window_name.replace('...', '')
        cmd = 'tmux switch-client -t \'{}\' \; select-window -t \'{}\''.format(
            window.session_name,
            window_name
        )
        subprocess.call(cmd, shell=True)

    def display(self):
        table = PrettyTable(['index', 'session', 'window'])
        table.align = 'l'
        table.align['index'] = 'c'
        table.padding_width = 2
        for index, window in enumerate(self.filter_windows):
            index = index + 1
            table.add_row([index, window.session_name, window.window_name])
        return table


class TmuxWindow(object):
    def __init__(self, session_name, window_name):
        self.session_name = session_name
        self.window_name = window_name
