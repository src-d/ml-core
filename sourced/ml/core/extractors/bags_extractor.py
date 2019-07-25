import bblfsh.compat as bblfsh

from sourced.ml.core.algorithms.token_parser import NoopTokenParser
from sourced.ml.core.algorithms.uast_to_role_id_pairs import Uast2RoleIdPairs
from sourced.ml.core.utils.pickleable_logger import PickleableLogger


class Extractor(PickleableLogger):
    """
    Converts a single UAST via `algorithm` to anything you need.
    It is a wrapper to use in `Uast2Features` Transformer in a pipeline.
    """
    NAME = None  # feature scheme name, should be overridden in the derived class.
    ALGORITHM = None  # algorithm class to extract from UAST
    OPTS = {}  # cmdline args which are passed into __init__()

    def _get_log_name(self):
        return type(self).__name__

    @classmethod
    def get_kwargs_fromcmdline(cls, args):
        prefix = cls.NAME + "_"
        result = {}
        for k, v in args.__dict__.items():
            if k.startswith(prefix):
                result[k[len(prefix):]] = v
        return result

    def extract(self, uast: bblfsh.Node):
        yield from self.ALGORITHM(uast)


class BagsExtractor(Extractor):
    """
    Converts a single UAST into the weighted set (dictionary), where elements are strings
    and the values are floats. The derived classes must implement uast_to_bag().
    """
    DEFAULT_DOCFREQ_THRESHOLD = 5
    NAMESPACE = None  # the beginning of each element in the bag
    OPTS = {"weight": 1}  # cmdline args which are passed into __init__()

    def __init__(self, docfreq_threshold=None, weight=None, **kwargs):
        """
        :param docfreq_threshold: The minimum number of occurrences of an element to be included \
                                  into the bag
        :param weight: TF-IDF will be multiplied by this weight to change importance of specific \
                      bag extractor
        :param kwargs: Parameters for parent constructor.
        """
        super().__init__(**kwargs)
        if docfreq_threshold is None:
            docfreq_threshold = self.DEFAULT_DOCFREQ_THRESHOLD
        self.docfreq_threshold = docfreq_threshold
        self.docfreq = {}
        self._ndocs = 0
        if weight is None:
            self.weight = 1
        else:
            self.weight = weight

    @property
    def docfreq_threhold(self):
        return self._docfreq_threshold

    @docfreq_threhold.setter
    def docfreq_threshold(self, value):
        if not isinstance(value, int):
            raise TypeError("docfreq_threshold must be an integer, got %s" % type(value))
        if value < 1:
            raise ValueError("docfreq_threshold must be >= 1, got %d" % value)
        self._docfreq_threshold = value

    @property
    def ndocs(self):
        return self._ndocs

    @ndocs.setter
    def ndocs(self, value):
        if not isinstance(value, int):
            raise TypeError("ndocs must be an integer, got %s" % type(value))
        if value < 1:
            raise ValueError("ndocs must be >= 1, got %d" % value)
        self._ndocs = value

    def extract(self, uast):
        for key, val in self.uast_to_bag(uast).items():
            yield self.NAMESPACE + key, val * self.weight

    def uast_to_bag(self, uast):
        raise NotImplementedError


class RoleIdsExtractor(Extractor):
    NAME = "roleids"
    ALGORITHM = Uast2RoleIdPairs(token_parser=NoopTokenParser())
