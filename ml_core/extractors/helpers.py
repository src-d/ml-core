import argparse
import inspect
from typing import List

from ml_core.extractors.bags_extractor import BagsExtractor

__extractors__ = {}


def register_extractor(cls):
    if not issubclass(cls, BagsExtractor):
        raise TypeError("%s is not an instance of %s" % (cls.__name__, BagsExtractor.__name__))
    __extractors__[cls.NAME] = cls
    return cls


def get_names_from_kwargs(func):
    for k, v in inspect.signature(func).parameters.items():
        if v.default != inspect.Parameter.empty and isinstance(
            v.default, (str, int, float, tuple)
        ):
            yield k.replace("_", "-"), v.default


def filter_kwargs(kwargs, func):
    func_param = inspect.signature(func).parameters.keys()
    return {k: v for k, v in kwargs.items() if k in func_param}


def create_extractors_from_args(args: argparse.Namespace) -> List[BagsExtractor]:
    return [
        __extractors__[s](
            args.min_docfreq,
            log_level=args.log_level,
            **__extractors__[s].get_kwargs_fromcmdline(args)
        )
        for s in args.feature
    ]
