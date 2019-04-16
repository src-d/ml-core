import string
import unittest

import numpy

from ml_core.tests import has_tensorflow


class MetricsTests(unittest.TestCase):
    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_register_metric(self):
        from sourced.ml.algorithms.id_splitter.nn_model import register_metric, METRICS
        fake_metric = "fake metric"
        register_metric(fake_metric)
        self.assertIn(fake_metric, METRICS)
        METRICS.pop()
        self.assertNotIn(fake_metric, METRICS)

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_raise_register_metric(self):
        from sourced.ml.algorithms.id_splitter.nn_model import register_metric, METRICS
        bad_metric = 1
        with self.assertRaises(AssertionError):
            register_metric(bad_metric)
        self.assertNotIn(bad_metric, METRICS)


class ModelsTests(unittest.TestCase):
    def setUp(self):
        from sourced.ml.algorithms.id_splitter.nn_model import build_rnn, build_cnn
        self.n_uniq = len(string.ascii_lowercase)
        self.model_rnn = build_rnn(maxlen=5, units=24, stack=2, rnn_layer="LSTM",
                                   optimizer="Adam", dev0="/cpu:0", dev1="/cpu:0")
        self.model_cnn = build_cnn(maxlen=5, filters=[64, 32, 16, 8], output_n_filters=32,
                                   stack=2, kernel_sizes=[2, 4, 8, 16], optimizer="Adam",
                                   device="/cpu:0")

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_build_rnn(self):
        self.assertTrue(self.model_rnn.built)
        self.assertTrue(self.model_rnn.trainable)
        self.assertIsInstance(self.model_rnn.get_weights()[0], numpy.ndarray)
        self.assertEqual(self.model_rnn.get_weights()[0].shape, (self.n_uniq+1, self.n_uniq+1))
        self.assertTrue(self.model_rnn.uses_learning_phase)

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_build_cnn(self):
        self.assertTrue(self.model_cnn.built)
        self.assertTrue(self.model_cnn.trainable)
        self.assertIsInstance(self.model_cnn.get_weights()[0], numpy.ndarray)
        self.assertEqual(self.model_cnn.get_weights()[0].shape, (self.n_uniq+1, self.n_uniq+1))
        self.assertTrue(self.model_cnn.uses_learning_phase)


if __name__ == "__main__":
    unittest.main()
