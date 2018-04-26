#!/usr/bin/python
# -*- coding: utf-8 -*-

def abbreviate(text, max_len):
    if len(text) <= max_len:
        return text

    return text[:max_len - 1] + u'⋯'
