from sourced.ml.core.algorithms.uast.inttypes_to_graphlets import Uast2GraphletBag
from sourced.ml.core.extractors import (
    BagsExtractor,
    filter_kwargs,
    get_names_from_kwargs,
    register_extractor,
)


@register_extractor
class GraphletBagExtractor(BagsExtractor):
    NAME = "graphlet"
    NAMESPACE = "g."
    OPTS = dict(get_names_from_kwargs(Uast2GraphletBag.__init__))
    OPTS.update(BagsExtractor.OPTS)

    def __init__(self, docfreq_threshold=None, **kwargs):
        original_kwargs = kwargs
        uast2bag_kwargs = filter_kwargs(kwargs, Uast2GraphletBag.__init__)
        for k in uast2bag_kwargs:
            kwargs.pop(k)
        super().__init__(docfreq_threshold, **kwargs)
        self._log.debug("__init__ %s", original_kwargs)
        uast2bag_kwargs = filter_kwargs(kwargs, Uast2GraphletBag.__init__)
        self.uast2bag = Uast2GraphletBag(**uast2bag_kwargs)

    def uast_to_bag(self, uast):
        return self.uast2bag(uast)
