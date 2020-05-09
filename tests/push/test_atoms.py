import pytest

from pyshgp.push.atoms import CodeBlock, Literal
from pyshgp.push.types import PushStr


class TestCodeBlock:

    def test_with_code_inserted_at_point(self):
        code_block = CodeBlock([
            CodeBlock([
                Literal(value="A", push_type=PushStr),
                Literal(value="B", push_type=PushStr)
            ]),
            Literal(value="C", push_type=PushStr)
        ])
        code = Literal(value="Z", push_type=PushStr)

        assert code_block.with_code_inserted_at_point(code, 0) == CodeBlock([
            code,
            CodeBlock([
                Literal(value="A", push_type=PushStr),
                Literal(value="B", push_type=PushStr)
            ]),
            Literal(value="C", push_type=PushStr)
        ])

        assert code_block.with_code_inserted_at_point(code, 1) == CodeBlock([
            CodeBlock([
                code,
                Literal(value="A", push_type=PushStr),
                Literal(value="B", push_type=PushStr)
            ]),
            Literal(value="C", push_type=PushStr)
        ])

        assert code_block.with_code_inserted_at_point(code, 2) == CodeBlock([
            CodeBlock([
                Literal(value="A", push_type=PushStr),
                code,
                Literal(value="B", push_type=PushStr)
            ]),
            Literal(value="C", push_type=PushStr)
        ])

        assert code_block.with_code_inserted_at_point(code, 3) == CodeBlock([
            CodeBlock([
                Literal(value="A", push_type=PushStr),
                Literal(value="B", push_type=PushStr),
                code
            ]),
            Literal(value="C", push_type=PushStr)
        ])

        assert code_block.with_code_inserted_at_point(code, 4) == CodeBlock([
            CodeBlock([
                Literal(value="A", push_type=PushStr),
                Literal(value="B", push_type=PushStr)
            ]),
            code,
            Literal(value="C", push_type=PushStr)
        ])

        assert code_block.with_code_inserted_at_point(code, 5) == CodeBlock([
            CodeBlock([
                Literal(value="A", push_type=PushStr),
                Literal(value="B", push_type=PushStr)
            ]),
            Literal(value="C", push_type=PushStr),
            code
        ])

        assert code_block.with_code_inserted_at_point(code, 100) == CodeBlock([
            CodeBlock([
                Literal(value="A", push_type=PushStr),
                Literal(value="B", push_type=PushStr)
            ]),
            Literal(value="C", push_type=PushStr),
            code
        ])

