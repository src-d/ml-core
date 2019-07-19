from collections import defaultdict
from typing import Dict

import bblfsh.compat as bblfsh

from sourced.ml.core.utils.bblfsh import iterate_children


class Uast2BagBase:
    """
    Base class to convert UAST to a bag of anything.
    """
    def __call__(self, uast: bblfsh.Node):
        """
        Inheritors must implement this function.

        :param uast: The UAST root node.
        """
        raise NotImplementedError


class Uast2BagThroughSingleScan(Uast2BagBase):
    """
    Constructs the bag by doing a single tree traversal and turning every node into a string.
    """
    def __call__(self, uast: bblfsh.Node) -> Dict[str, int]:
        result = defaultdict(int)
        stack = [uast]
        while stack:
            node = stack.pop()
            stack.extend(iterate_children(node.children))
            result[self.node2key(node)] += 1
        return result

    def node2key(self, node) -> str:
        raise NotImplementedError
