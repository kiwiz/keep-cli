import gkeepapi
from typing import List

class Query(object):
    @classmethod
    def fromConfig(cls, config: dict) -> 'Query':
        query = config.get('query')
        labels = config.get('labels')
        colors = config.get('colors')
        pinned = config.get('pinned')
        archived = config.get('archived', False)
        trashed = config.get('trashed', False)

        return cls(query, labels, colors, pinned, archived, trashed)

    def __init__(self, query=None, labels=None, colors=None, pinned=None, archived=False, trashed=False):
        self.query = query
        self.labels = labels
        self.colors = colors
        self.pinned = pinned
        self.archived = archived
        self.trashed = trashed

    def filter(self, keep: gkeepapi.Keep) -> List[gkeepapi.node.TopLevelNode]:
        return keep.find(
            query=self.query,
            labels=self.labels,
            colors=self.colors,
            pinned=self.pinned,
            archived=self.archived,
            trashed=self.trashed
        )
