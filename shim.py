import urwid
import logging

logging.basicConfig(filename='debug.log')

str_util = urwid.escape.str_util

def get_width(c):
    if c == '📍':
        return 2
    str_util._get_width(c)

def patch():
    str_util._get_width = str_util.get_width
    str_util.get_width = get_width
