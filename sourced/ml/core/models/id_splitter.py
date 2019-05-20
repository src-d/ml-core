import string
from typing import Dict, List, Sequence, Tuple

from modelforge import Model, register_model
import numpy
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences

from sourced.ml.core.algorithms.id_splitter.nn_model import (f1score, precision,
                                                             recall)
from sourced.ml.core.models.license import DEFAULT_LICENSE


@register_model
class IdentifierSplitterBiLSTM(Model):
    """
    Bidirectional LSTM Model. Splits identifiers without need for a conventional pattern.
    Reference: https://arxiv.org/abs/1805.11651
    """
    NAME = "id_splitter_bilstm"
    VENDOR = "source{d}"
    DESCRIPTION = "Weights of the BiLSTM network to split source code identifiers."
    LICENSE = DEFAULT_LICENSE

    DEFAULT_MAXLEN = 40
    DEFAULT_PADDING = "post"
    DEFAULT_MAPPING = {c: i for i, c in enumerate(string.ascii_lowercase, start=1)}
    DEFAULT_BATCH_SIZE = 4096

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._maxlen = self.DEFAULT_MAXLEN
        self._padding = self.DEFAULT_PADDING
        self._mapping = self.DEFAULT_MAPPING
        self._model = None
        self._batch_size = self.DEFAULT_BATCH_SIZE

    def construct(self, model: "keras.models.Model",
                  maxlen: int = DEFAULT_MAXLEN,
                  padding: str = DEFAULT_PADDING,
                  mapping: Dict[str, int] = DEFAULT_MAPPING,
                  batch_size: int = DEFAULT_BATCH_SIZE) -> "IdentifierSplitterBiLSTM":
        """
        :param model: keras model used for identifier splitting.
        :param maxlen: maximum length of input identifers.
        :param padding: where to pad the identifiers of length < maxlen. Can be "left" or "right".
        :param mapping: mapping of characters to integers.
        :param batch_size: batch size of input data fed to the model.
        :return: BiLSTM based source code identifier splitter.
        """

        self._maxlen = maxlen
        self._padding = padding
        self._mapping = mapping
        self._model = model
        self._batch_size = batch_size

        return self

    @property
    def model(self) -> "keras.models.Model":
        """
        Returns the wrapped keras model.
        """
        return self._model

    @property
    def batch_size(self) -> int:
        """
        Returns the batch size used to run the model
        """
        return self._batch_size

    def _generate_tree(self) -> dict:
        return {
            "config": self._model.get_config(),
            "weights": self._model.get_weights(),
            "mapping": self._mapping,
            "maxlen": self._maxlen,
            "padding": self._padding,
            }

    def _load_tree(self, tree: dict):
        model = keras.models.Model.from_config(tree["config"])
        model.set_weights(tree["weights"])
        self.construct(model, maxlen=tree["maxlen"],
                       padding=tree["padding"], mapping=tree["mapping"])

    def _prepare_single_identifier(self, identifier: str) -> Tuple[numpy.array, str]:
        # Clean identifier
        clean_id = "".join(char for char in identifier.lower() if char in self._mapping)
        if len(clean_id) > self._maxlen:
            clean_id = clean_id[:self._maxlen]
        self._log.debug("Preprocessed identifier: %s : %s" % (identifier, clean_id))
        return numpy.array([self._mapping[c] for c in clean_id]), clean_id

    def prepare_input(self, identifiers: Sequence[str]) -> Tuple[numpy.array, List[str]]:
        """
        Prepare input by converting a sequence of identifiers to the corresponding
        ascii code 2D-array and the list of lowercase cleaned identifiers.
        """
        processed_ids = []
        clean_ids = []
        for identifier in identifiers:
            feat, clean_id = self._prepare_single_identifier(identifier)
            processed_ids.append(feat)
            clean_ids.append(clean_id)

        processed_ids = pad_sequences(processed_ids, maxlen=self._maxlen, padding=self._padding)
        return processed_ids, clean_ids

    def load_model_file(self, path: str):
        """
        Loads a compatible Keras model file. Used for compatibility.
        """
        self._model = keras.models.load_model(path, custom_objects={"precision": precision,
                                                                    "recall": recall,
                                                                    "f1score": f1score})

    def split(self, identifiers: Sequence[str]) -> List[str]:
        """
        Splits a lists of identifiers using the model.
        """
        feats, clean_ids = self.prepare_input(identifiers)
        output = self._model.predict(feats, batch_size=self._batch_size)
        output = numpy.round(output)[:, :, 0]
        splitted_ids = []
        for clean_id, id_output in zip(clean_ids, output):
            splitted_id = ""
            for char, label in zip(clean_id, id_output):
                if label == 1:
                    splitted_ids.append(splitted_id)
                    splitted_id = ""
                splitted_id += char
            splitted_ids.append(splitted_id)
        return splitted_ids
