from typing import Sequence, List

from pyrsistent import PRecord, field

from pyshgp.push.config import PushConfig
from pyshgp.push.atoms import CodeBlock
from pyshgp.utils import Saveable


class ProgramSignature(PRecord):
    arity = field(type=int, mandatory=True)
    output_stacks = field(type=list, mandatory=True)
    push_config = field(type=PushConfig, mandatory=True)


class Program(Saveable, PRecord):
    code = field(type=CodeBlock, mandatory=True)
    signature = field(type=ProgramSignature, mandatory=True)
