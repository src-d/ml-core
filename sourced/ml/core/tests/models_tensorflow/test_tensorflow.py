import io
import unittest

from sourced.ml.core.models.tensorflow import TensorFlowModel
from sourced.ml.core.tests import has_tensorflow


class TensorFlowModelTests(unittest.TestCase):
    @unittest.skipIf(not has_tensorflow(), "Tensorflow is not installed.")
    def test_serialize(self):
        import tensorflow as tf

        a = tf.constant([[1, 0], [0, 1]])
        b = tf.constant([[0, 1], [1, 0]])
        c = tf.matmul(a, b)
        gd = tf.get_default_graph().as_graph_def()
        buffer = io.BytesIO()
        TensorFlowModel().construct(graphdef=gd).save(buffer, series="tensorflow-model")
        buffer.seek(0)
        model = TensorFlowModel().load(buffer)
        self.assertEqual(gd.node, model.graphdef.node)

        buffer = io.BytesIO()
        with tf.Session() as session:
            TensorFlowModel().construct(session=session, outputs=[c.name[:-2]]).save(
                buffer, series="tensorflow-model"
            )
        buffer.seek(0)
        model = TensorFlowModel().load(buffer)
        self.assertEqual(gd.node, model.graphdef.node)


if __name__ == "__main__":
    unittest.main()
