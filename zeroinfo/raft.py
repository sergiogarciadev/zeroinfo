# -*- coding: utf-8 -*-
"""Raft classes."""

import random

from collections import OrderedDict
from typing import List


def term_timeout():
    # between 150 and 300
    return random.random() * 0.150 + 0.150


class Entry(object):
    def __init__(self, index: int, term: int):
        self.index = index
        self.term = term


class State(object):
    """Common state for all servers."""

    def __init__(self):
        self._current_term = 0
        self._voted_for = None
        self._log = OrderedDict()
        self._commit_index = 0
        self._last_applied = 0

        self._next_index = []
        self._match_index = []

    def after_new_election(self):
        """Refresh state after a new election."""

        self._next_index = []
        self._match_index = []

    def append_entries(self, term: int, leader_id: int, prev_log_index: int,
                       prev_log_term: int, entries: List[Entry], leader_commit: int):
        if term < self._current_term:
            return (self._current_term, False)

        if prev_log_index not in self._log:
            return (self._current_term, False)

        if self._log[prev_log_index] != prev_log_term:
            return (self._current_term, False)

        if len(entries) == 0:
            # just a heartbeat
            return

        for entry in entries:
            if entry.index in self._log:
                keys_to_remove = [key for key in list(self._log.keys()) if key >= entry.index]
                for key in keys_to_remove:
                    del self._log[key]

        for entry in entries:
            self._log[entry.index] = entry

        if leader_commit > self._commit_index:
            self._commit_index = min([leader_commit, entries[-1].index])

        return (self._current_term, True)

    def request_vote(self, term: int, candidate_id: int, last_log_index: int, last_log_term: int):
        if term < self._current_term:
            return (term, False)

        if self._voted_for is None or self._voted_for == candidate_id:
            if last_log_index >= self._commit_index:
                self._voted_for = candidate_id
                return (term, True)

    def rules(self, term: int):
        # all servers
        if self._commit_index > self._last_applied:
            # self._log[self._last_applied]
            pass

        if term > self._current_term:
            # now set this node to a follower
            self._current_term = term

        # if timeouted this node becames a candidate