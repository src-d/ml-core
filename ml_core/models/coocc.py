from modelforge.model import (
    assemble_sparse_matrix, disassemble_sparse_matrix, merge_strings, Model, split_strings)
from modelforge.models import register_model

from ml_core.models.license import DEFAULT_LICENSE


@register_model
class Cooccurrences(Model):
    """
    Co-occurrence matrix.
    """
    NAME = "co-occurrences"
    VENDOR = "source{d}"
    DESCRIPTION = "Model that contains the sparse co-occurrence matrix of source code identifiers."
    LICENSE = DEFAULT_LICENSE

    def construct(self, tokens, matrix):
        self._tokens = tokens
        self._matrix = matrix
        return self

    def _load_tree(self, tree):
        self.construct(tokens=split_strings(tree["tokens"]),
                       matrix=assemble_sparse_matrix(tree["matrix"]))

    def dump(self):
        return """Number of words: %d
First 10 words: %s
Matrix: shape: %s non-zero: %d""" % (
            len(self.tokens), self.tokens[:10], self.matrix.shape, self.matrix.getnnz())

    @property
    def tokens(self):
        """
        Returns the tokens in the order which corresponds to the matrix's rows and cols.
        """
        return self._tokens

    @property
    def matrix(self):
        """
        Returns the sparse co-occurrence matrix.
        """
        return self._matrix

    def __len__(self):
        """
        Returns the number of tokens in the model.
        """
        return len(self._tokens)

    def _generate_tree(self):
        return {"tokens": merge_strings(self.tokens),
                "matrix": disassemble_sparse_matrix(self.matrix)}

    def matrix_to_rdd(self, spark_context: "pyspark.SparkContext") -> "pyspark.RDD":
        self._log.info("Convert coocc model to RDD...")
        rdd_row = spark_context.parallelize(self._matrix.row)
        rdd_col = spark_context.parallelize(self._matrix.col)
        rdd_data = spark_context.parallelize(self._matrix.data)
        return rdd_row.zip(rdd_col).zip(rdd_data)
