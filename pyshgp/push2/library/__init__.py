from pyshgp.push2.instruction import *

INSTRUCTIONS: Dict[str, Instruction] = {}


def register(
    name: str,
    inputs: Tuple[StackRef, ...],
    outputs: Tuple[StackRef, ...],
    invariants: Sequence[Callable[[Any, ...], bool]] = None,
    blocks: int = 0,
    docstring: str = "Write me!"
):
    def decorator(func):
        meta = InstructionMeta(name, blocks, docstring)
        instr = SimpleInstruction(meta, func, inputs, outputs, invariants)
        INSTRUCTIONS[name] = instr
        return func

    return decorator


def register_class(name: str, blocks: int = 0, docstring: str = "Write me!", *args, **kwargs):
    def decorator(cls: type):
        meta = InstructionMeta(name, blocks, docstring)
        INSTRUCTIONS[name] = cls(meta, *args, **kwargs)
        return cls

    return decorator
