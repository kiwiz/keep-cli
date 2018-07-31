#!/usr/bin/python
# -*- coding: utf-8 -*-

def abbreviate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text

    return text[:max_len - 1] + u'⋯'
