# TODO (Guillemdb): fix imports
from ml_core.algorithms.uast.uast_struct_to_bag import UastRandomWalk2Bag
from ml_core.extractors.bags_extractor import BagsExtractor
from ml_core.extractors.helpers import filter_kwargs, get_names_from_kwargs, register_extractor


@register_extractor
class UastRandomWalkBagExtractor(BagsExtractor):
    NAME = "node2vec"
    NAMESPACE = "r."
    OPTS = dict(get_names_from_kwargs(UastRandomWalk2Bag.__init__))
    OPTS.update(BagsExtractor.OPTS)

    def __init__(self, docfreq_threshold=None, **kwargs):
        original_kwargs = kwargs
        uast2bag_kwargs = filter_kwargs(kwargs, UastRandomWalk2Bag.__init__)
        for k in uast2bag_kwargs:
            kwargs.pop(k)
        super().__init__(docfreq_threshold, **kwargs)
        self._log.debug("__init__ %s", original_kwargs)
        self.uast2bag = UastRandomWalk2Bag(**uast2bag_kwargs)

    def uast_to_bag(self, uast):
        return self.uast2bag(uast)
