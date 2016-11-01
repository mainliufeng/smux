# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


help_text = u"""
note of command

list mode
q:      quit
s:      search mode
h:      help mode
?:      help mode
a:      add mode
e:      edit mode
d:      delete mode
n:      next page
p:      previous page

help mode
h:      return to list mode
?:      return to list mode
esc:    return to list mode

edit mode
n:      next page
p:      previous page
0-9:    edit command note
esc:    return to list mode

delete mode
n:      next page
p:      previous page
0-9:    delete command note
esc:    return to list mode

search mode
esc:    return to list mode
"""
