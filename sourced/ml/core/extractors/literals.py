import codecs
from collections import defaultdict
import os

# TODO (Guillemdb): fix imports
from sourced.ml.core.algorithms.uast.ids_to_bag import uast2sequence, UastIds2Bag
from sourced.ml.core.extractors.bags_extractor import BagsExtractor
from sourced.ml.core.extractors.helpers import register_extractor
from sourced.ml.core.utils import bblfsh_roles


class HashedTokenParser:
    def process_token(self, token):
        yield codecs.encode(
            (hash(token) & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little"), "hex_codec"
        ).decode()


class Literals2Bag(UastIds2Bag):
    """
    Converts a UAST to a bag-of-literals.
    """

    XPATH = "//*[@roleLiteral]"

    def __init__(self, token2index=None, token_parser=None):
        """
        :param token2index: The mapping from tokens to bag keys. If None, no mapping is performed.
        :param token_parser: Specify token parser if you want to use a custom one. \
            :class:'TokenParser' is used if it is not specified.
        """
        token_parser = HashedTokenParser() if token_parser is None else token_parser
        super().__init__(token2index, token_parser)

    def __call__(self, uast):
        """
        HOTFIX for https://github.com/bblfsh/client-python/issues/92
        Converts a UAST to a weighed bag-of-literals. The weights are literals frequencies.
        The tokens are preprocessed by _token_parser.
        Overwrite __call__ to avoid issues with `bblfsh.filter`.

        :param uast: The UAST root node.
        :return: bag
        """
        nodes = [node for node in uast2sequence(uast) if bblfsh_roles.LITERAL in node.roles]
        bag = defaultdict(int)
        for node in nodes:
            for sub in self._token_parser.process_token(node.token):
                try:
                    bag[self._token2index[sub]] += 1
                except KeyError:
                    continue
        return bag


@register_extractor
class LiteralsBagExtractor(BagsExtractor):
    NAME = "lit"
    NAMESPACE = "l."
    OPTS = BagsExtractor.OPTS.copy()

    def __init__(self, docfreq_threshold=None, **kwargs):
        super().__init__(docfreq_threshold, **kwargs)
        self.id2bag = Literals2Bag(None, HashedTokenParser())

    def uast_to_bag(self, uast):
        if os.getenv("PYTHONHASHSEED", "random") == "random":
            raise RuntimeError("PYTHONHASHSEED must be set")
        return self.id2bag(uast)
