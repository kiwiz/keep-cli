import copy
import logging
import gkeepapi
import typing
from typing import List, Optional, Union

logger = logging.getLogger('keep-cli')

class Query(object):
    @classmethod
    def fromConfig(cls, keep: gkeepapi.Keep, config: dict) -> 'Query':
        config = copy.deepcopy(config)

        name = config.get('name', '')
        query = config.get('query')
        labels = None
        colors = None
        pinned = config.get('pinned')
        archived = config.get('archived', False)
        trashed = config.get('trashed', False)

        if 'labels' in config:
            labels = []
            raw = config.get('labels', [])

            if raw:
                for i in raw:
                    l = keep.findLabel(i)
                    labels.append(l)
                    if l is None:
                        logger.warn('Label not found: %s', i)
            config['labels'] = labels

        if 'colors' in config:
            colors = []

            for i in config.get('colors', []):
                try:
                    c = gkeepapi.node.ColorValue(i.upper())
                    colors.append(c)
                except ValueError:
                    logger.warn('Color not found: %s', i)
            config['colors'] = colors

        return cls(name, query, labels, colors, pinned, archived, trashed)

    def __init__(
        self,
        name: str='',
        query: Optional[Union[str, typing.re.Pattern]]=None,
        labels: Optional[List[gkeepapi.node.Label]]=None,
        colors: Optional[List[gkeepapi.node.ColorValue]]=None,
        pinned: Optional[bool]=None,
        archived: Optional[bool]=False,
        trashed: Optional[bool]=False
    ):
        self.name = name
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
