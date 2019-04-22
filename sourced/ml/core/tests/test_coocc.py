import unittest

from sourced.ml.core.models.coocc import Cooccurrences
import sourced.ml.core.tests.models as paths


class CooccurrencesTests(unittest.TestCase):
    def setUp(self):
        self.model = Cooccurrences().load(source=paths.COOCC)

    def test_tokens(self):
        tokens = self.model.tokens
        self.assertIsInstance(tokens, list)
        self.assertEqual(
            tokens[:10],
            [
                "i.set",
                "i.iter",
                "i.error",
                "i.logsdir",
                "i.read",
                "i.captur",
                "i.clear",
                "i.android",
                "i.tohome",
                "i.ljust",
            ],
        )
        self.assertEqual(len(tokens), 304)

    def test_matrix(self):
        matrix = self.model.matrix
        self.assertEqual(matrix.shape, (304, 304))
        self.assertEqual(matrix.getnnz(), 16001)

    def test_len(self):
        self.assertEqual(len(self.model), 304)


if __name__ == "__main__":
    unittest.main()
