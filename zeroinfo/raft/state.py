# -*- coding: utf-8 -*-
"""Raft entries."""

import asyncio
import random

from collections import OrderedDict


def get_term_timeout():
    """Return term timeout (between 150 and 300 ms)."""

    return random.random() * 0.150 + 0.150


class State(object):
    """Common state for all servers."""

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        self.log = OrderedDict()
        self.current_term = 0
        self.commit_index = 0
        self.last_applied = 0

        self._timeout_handler = None

    def set_timeout(self):
        """Set a trigger for term timeout."""

        if self._timeout_handler is not None:
            self._timeout_handler.cancel()
        self._timeout_handler = self.loop.call_later(get_term_timeout(), self.on_timeout)

    def on_timeout(self):
        """Callback called when a term got timeouted."""

        self.set_timeout()
        from datetime import datetime
        print(f'{datetime.now()} on timeout')


class FollowerState(State):
    """Follower state."""

    def __init__(self):
        super().__init__(self)


class CandidateState(State):
    """Candidate state."""

    def __init__(self):
        super().__init__(self)


class LeaderState(State):
    """Leader state."""

    def __init__(self):
        super().__init__(self)
