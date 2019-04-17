from typing import Iterable

import bblfsh

from ml_core.algorithms.token_parser import NoopTokenParser
from ml_core.algorithms.uast.to_id_sequence import Uast2IdSequence
from ml_core.extractors.bags_extractor import BagsExtractor


class IdSequenceExtractor(BagsExtractor):
    """
    Extractor wrapper for Uast2RoleIdPairs algorithm.
    Note that this is unusual BagsExtractor since it returns iterable instead of bag.

    The class did not wrap with @register_extractor because it does not produce bags as others do.
    So nobody outside code will see it or use it directly.
    For the same reason we a free to override NAMESPACE, NAME, OPTS fields with any value we want.

    TODO(zurk): Split BagsExtractor into two clases: Extractor and BagsExtractor(Extractor),
    re-inherit this class from Extractor, delete explanations from docstring.
    """

    NAMESPACE = ""
    NAME = "id sequence"
    OPTS = {}

    def __init__(self, split_stem=False, **kwargs):
        super().__init__(**kwargs)
        self.uast2id_sequence = Uast2IdSequence(
            None, NoopTokenParser() if not split_stem else None
        )

    def extract(self, uast: bblfsh.Node) -> Iterable[str]:
        yield self.uast2id_sequence(uast), None
