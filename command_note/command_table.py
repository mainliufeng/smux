# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import json
import math

from prettytable import PrettyTable
from fuzzywuzzy import process


CMD_PATH = os.path.join(os.getenv('HOME'), '.cmd')
PAGE_SIZE = 10


class CommandTable(object):

    def __init__(self):
        # 过滤重复的命令
        self.all_cmd_note_list = []
        cmd_set = set()
        for cmd_note in cmd_note_generate():
            if cmd_note.cmd not in cmd_set:
                cmd_set.add(cmd_note.cmd)
                self.all_cmd_note_list.append(cmd_note)
        # query过滤后的命令列表
        self.cmd_note_list = self.all_cmd_note_list
        self.query = ''
        self.page_size = PAGE_SIZE
        self._refresh_page_info()

        self.search_key_list = []
        self.search_key_cmd_note_dict = {}
        for cmd_note in self.all_cmd_note_list:
            search_key = u'{}: {}'.format(cmd_note.note, cmd_note.cmd)
            self.search_key_list.append(search_key)
            self.search_key_cmd_note_dict[search_key] = cmd_note

    # page operations
    def get_page_info(self):
        return self.current_page, self.page_count

    def next_page(self):
        if self.current_page < self.page_count:
            self.current_page += 1

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    # command operations
    def get_cmd(self, index):
        cmd_note = self.get_cmd_note(index)
        if cmd_note is not None:
            return cmd_note.cmd

    def get_cmd_note(self, index):
        if index < self.page_size and index >= 0:
            try:
                return self.cmd_note_list[
                    (self.current_page-1)*self.page_size + index
                ]
            except IndexError:
                pass

    def delete_cmd_note(self, index):
        if index < self.page_size and index >= 0:
            try:
                del self.cmd_note_list[
                    (self.current_page-1)*self.page_size + index
                ]
                self._refresh_page_info()
                save_cmd_notes(self.all_cmd_note_list)
            except IndexError:
                pass

    def edit_cmd_note(self, index, cmd_note):
        if index < self.page_size and index >= 0:
            try:
                origin_cmd_note = self.cmd_note_list[
                    (self.current_page-1)*self.page_size + index
                ]
                origin_cmd_note.cmd = cmd_note.cmd
                origin_cmd_note.note = cmd_note.note
                save_cmd_notes(self.all_cmd_note_list)
            except IndexError:
                pass

    def add_cmd_note(self, cmd_note):
        self.all_cmd_note_list.append(cmd_note)
        self._refresh_page_info()
        save_cmd_notes(self.all_cmd_note_list)

    def get_cmd_table(self):
        offset = (self.current_page - 1) * self.page_size
        limit = self.page_size

        table = PrettyTable(['index', 'name', 'command'])
        table.align = 'l'
        table.align['index'] = 'c'
        table.padding_width = 2
        for index, t in enumerate(
            self.cmd_note_list[offset: offset + limit]
        ):
            table.add_row([index, t.note, t.cmd])

        return table

    # search operations
    def get_query(self):
        return self.query

    def set_query(self, query):
        origin_query = self.query

        self.query = query
        self._do_search()

        if origin_query != self.query:
            self._refresh_page_info()

    def _do_search(self):
        if not self.query:
            self.cmd_note_list = self.all_cmd_note_list
        else:
            search_key_score_list = process.extract(
                self.query,
                self.search_key_list,
                limit=len(self.all_cmd_note_list)
            )
            self.cmd_note_list = [
                self.search_key_cmd_note_dict[search_key_score[0]]
                for search_key_score in search_key_score_list
            ]

    def _refresh_page_info(self):
        self.page_count = int(math.ceil(
            len(self.cmd_note_list) / float(self.page_size)
        ))
        self.current_page = 1


class CommandNote(object):

    def __init__(self, cmd, note):
        self.cmd = cmd
        self.note = note


def cmd_note_generate():
    with open(cmd_path(), 'r') as f:
        content = f.read()
        note_json_list = content.split('\n')
        for note_json in filter(bool, note_json_list):
            note_cmd_tuple = json.loads(note_json)
            yield CommandNote(note_cmd_tuple[1], note_cmd_tuple[0])


def save_cmd_notes(cmd_note_list):
    with open(cmd_path(), 'w') as f:
        f.write(
            '\n'.join([
                json.dumps((cmd_note.note, cmd_note.cmd))
                for cmd_note in cmd_note_list
            ])
        )

def cmd_path():
    if not os.path.exists(CMD_PATH):
        with open(CMD_PATH, 'a') as f:
            pass
    return CMD_PATH
