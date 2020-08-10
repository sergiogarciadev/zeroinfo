# -*- coding: utf-8 -*-
"""Raft entries."""


class Entry(object):
    """Raft entry."""

    def __init__(self, index: int, term: int):
        self.index = index
        self.term = term

