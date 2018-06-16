import gkeepapi
from typing import List

class Query(object):
    def filter(self, keep: gkeepapi.Keep) -> List[gkeepapi.node.TopLevelNode]:
        return keep.find(archived=False)
