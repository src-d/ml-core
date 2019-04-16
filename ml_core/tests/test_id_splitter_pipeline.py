import tempfile
import unittest

import numpy

from ml_core.tests import has_tensorflow


class IdSplitterPipelineTest(unittest.TestCase):
    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_binarize(self):
        from sourced.ml.algorithms.id_splitter.pipeline import binarize

        thresholds = [0, 0.09, 0.19, 0.29, 0.39, 0.49, 0.59, 0.69, 0.79, 0.89, 0.99]
        n_pos = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

        for th, n_p in zip(thresholds, n_pos):
            vals = numpy.arange(10) / 10
            res = binarize(vals, th)
            self.assertEqual(sum(binarize(vals, th)), n_p)
            if th in (0, 0.99):
                self.assertEqual(numpy.unique(res).shape[0], 1)
            else:
                self.assertEqual(numpy.unique(res).shape[0], 2)

        vals = numpy.arange(10) / 10
        old_vals = vals.copy()
        for th, n_p in zip(thresholds, n_pos):
            res = binarize(vals, th, inplace=False)
            self.assertEqual(sum(res), n_p)
            self.assertTrue(numpy.array_equal(old_vals, vals))
            if th in (0, 0.99):
                self.assertEqual(numpy.unique(res).shape[0], 1)
            else:
                self.assertEqual(numpy.unique(res).shape[0], 2)

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_prepare_devices(self):
        from sourced.ml.algorithms.id_splitter.nn_model import prepare_devices

        correct_args = ["1", "0,1", "-1"]
        resulted_dev = [("/gpu:1", "/gpu:1"), ("/gpu:0", "/gpu:1"), ("/cpu:0", "/cpu:0")]
        for res, arg in zip(resulted_dev, correct_args):
            self.assertEqual(res, prepare_devices(arg))

        bad_args = ["", "1,2,3"]
        for arg in bad_args:
            with self.assertRaises(ValueError):
                prepare_devices(arg)

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_build_schedule(self):
        from sourced.ml.algorithms.id_splitter.pipeline import build_schedule

        start_lr = 10
        end_lr = 1
        n_epochs = 9

        lr_schedule = build_schedule(lr=start_lr, final_lr=end_lr, n_epochs=n_epochs)

        for i in range(n_epochs):
            self.assertEqual(start_lr - i, lr_schedule(epoch=i))

        with self.assertRaises(AssertionError):
            lr_schedule(-1)
        with self.assertRaises(AssertionError):
            lr_schedule(n_epochs + 1)

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_build_train_generator(self):
        from sourced.ml.algorithms.id_splitter.pipeline import build_train_generator

        batch_size = 3
        # mismatch number of samples
        bad_x = numpy.zeros(3)
        bad_y = numpy.zeros(4)
        with self.assertRaises(AssertionError):
            build_train_generator(bad_x, bad_y, batch_size=batch_size)

        # check generator with correct inputs
        x = numpy.zeros(5)
        gen = build_train_generator(x, x, batch_size=batch_size)
        expected_n_samples = [3, 2]
        for n_samples in expected_n_samples:
            x_gen, y_gen = next(gen)
            self.assertEqual(x_gen.shape, y_gen.shape)
            self.assertEqual(n_samples, x_gen.shape[0])

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_train_parameters(self):
        from sourced.ml.algorithms.id_splitter.pipeline import create_generator_params

        batch_size = 500
        samples_per_epoch = 10 ** 6
        n_samples = 40 * 10 ** 6
        epochs = 10

        steps_per_epoch_ = samples_per_epoch // batch_size
        n_epochs_ = numpy.ceil(epochs * n_samples / samples_per_epoch)

        steps_per_epoch, n_epochs = create_generator_params(
            batch_size, samples_per_epoch, n_samples, epochs
        )
        self.assertEqual(steps_per_epoch, steps_per_epoch_)
        self.assertEqual(n_epochs, n_epochs_)

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_config_keras(self):
        from keras.backend.tensorflow_backend import get_session
        from sourced.ml.algorithms.id_splitter.pipeline import config_keras

        config_keras()
        sess = get_session()
        self.assertTrue(sess._config.gpu_options.allow_growth)

    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_prepare_callbacks(self):
        from keras.callbacks import TensorBoard, CSVLogger, ModelCheckpoint
        from sourced.ml.algorithms.id_splitter.pipeline import prepare_callbacks

        with tempfile.TemporaryDirectory() as tmpdir:
            callbacks = prepare_callbacks(tmpdir)

            # TensorBoard
            self.assertIsInstance(callbacks[0], TensorBoard)
            self.assertTrue(callbacks[0].log_dir.startswith(tmpdir))

            # CSVLogger
            self.assertIsInstance(callbacks[1], CSVLogger)
            self.assertTrue(callbacks[1].filename.startswith(tmpdir))

            # ModelCheckpoint
            self.assertIsInstance(callbacks[2], ModelCheckpoint)
            self.assertTrue(callbacks[2].filepath.startswith(tmpdir))
