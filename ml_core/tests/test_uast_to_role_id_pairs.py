import unittest

from bblfsh import BblfshClient

from ml_core.algorithms.token_parser import NoopTokenParser
from ml_core.algorithms.uast.uast_to_role_id_pairs import Uast2RoleIdPairs
from ml_core.tests.models import SOURCE_PY


class Uast2NodesBagTest(unittest.TestCase):
    def setUp(self):
        self.uast2role_id_pairs = Uast2RoleIdPairs(token_parser=NoopTokenParser())
        self.uast = BblfshClient("0.0.0.0:9432").parse(SOURCE_PY).uast

    def test_result(self):
        correct = [
            ("ModuleSpec", "BODY | IF | THEN"),
            ("ModuleSpec", "IDENTIFIER | EXPRESSION | CALL | CALLEE"),
            ("ModuleSpec", "STATEMENT | INCOMPLETE"),
            ("__package__", "BINARY | EXPRESSION | CONDITION"),
            ("__spec__", "BINARY | EXPRESSION | CONDITION"),
            ("__spec__", "BODY | IF | THEN"),
            ("collections", "IDENTIFIER | IMPORT | PATHNAME"),
            ("modelforge.logs", "IDENTIFIER | IMPORT | PATHNAME"),
            ("modules", "RIGHT | EXPRESSION | INCOMPLETE"),
            ("namedtuple", "IDENTIFIER | EXPRESSION | CALL | CALLEE"),
            ("namedtuple", "IDENTIFIER | IMPORT | PATHNAME"),
            ("setup", "IDENTIFIER | DECLARATION | FUNCTION | NAME"),
            ("setup_logging", "IDENTIFIER | EXPRESSION | CALL | CALLEE"),
            ("setup_logging", "IDENTIFIER | IMPORT | PATHNAME"),
            ("sys", "IDENTIFIER | IMPORT | PATHNAME"),
            ("sys", "RIGHT | EXPRESSION | INCOMPLETE"),
            ("utmain", "BINARY | EXPRESSION | CONDITION"),
            ("utmain", "BINARY | EXPRESSION | CONDITION"),
            ("utmain", "BODY | IF | THEN"),
            ("utmain", "FILE | MODULE"),
            ("utmain", "STATEMENT | INCOMPLETE"),
        ]
        res = sorted(self.uast2role_id_pairs(self.uast))
        self.assertEqual(res, correct)


if __name__ == "__main__":
    unittest.main()
