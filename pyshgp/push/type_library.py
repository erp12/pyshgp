"""A PushTypeLibrary describes the PushTypes which a given instance of PushGP will support."""
from typing import Any, Sequence, Tuple, Optional, Set, Callable

from pyshgp.push.types import PushType, CORE_PUSH_TYPES
from pyshgp.push.atoms import Atom, Literal
from pyshgp.validation import PushError


RESERVED_PSEUDO_STACKS = {"untyped", "stdout"}


class PushTypeLibrary(dict):
    """A collection of PushTypes which can support a corresponding PushStack.

    Parameters
    ----------
    register_core : bool, optional
        If True, all core types will be registered. Default is True.
    *args
        A collection of PushTypes to register.

    Attributes
    ----------
    register_core : bool, optional
        If True, all core types will be registered. Default is True.
    *args
        A collection of PushTypes to register.

    """

    def __init__(self, register_core: bool = True, *args):
        super().__init__()
        if register_core:
            self.register_core()
        self.register_list(args)
        self.create_and_register("code", (Atom, ), force=True)
        self.create_and_register("exec", (Atom, ), force=True)

    def register(self, push_type: PushType, _force=False):
        """Register a PushType object.

        Parameters
        ----------
        push_type
            PushType to register.
        _force : bool, optional
            For internal use only. Default is False.

        Returns
        -------
        PushTypeLibrary
            A reference to the ``PushTypeLibrary``.

        """
        name = push_type.name
        if (not _force) and (name in RESERVED_PSEUDO_STACKS):
            raise ValueError("Cannot register PushType with name {nm} because it is reserved.".format(nm=name))
        self[name] = push_type
        return self

    def create_and_register(self,
                            name: str,
                            underlying_types: Tuple[type],
                            is_collection: bool = False,
                            is_numeric: bool = False,
                            coercion_func: Optional[Callable[[Any], Any]] = None,
                            force=False):
        """Create a PushType and register it into the library.

        Parameters
        ----------
        name : str
            A name for the type. Used when referencing the PushType in Instruction
            definitions and will be the key in the PushState for the corresponding
            PushStack.
        underlying_types : Tuple[type]
            A tuple of python types that correspond to the underlying
            native types which the PushType is representing.
        is_collection : bool, optional
            Indicates if the PushType is a collection. Default is False.
        is_numeric : bool, optional
            Indicates if the PushType is a number. Default is False.
        coercion_func : Callable[[Any], Any], optional
            A function which takes a single argument and returns argument coerced
            into the PushTypes canonical type (the first type in ``underlying``).
            If None, the constructor of the canonical type is used. Default is None.
        force : bool
            If True, will register the type even if it will overwrite an
            existing reserved stack typed (eg. exec, stdout, untyped). Default
            is False. It is not reccomended this argument be changed unless
            you have a very good reason to do so.

        Returns
        -------
        PushTypeLibrary
            A reference to the PushTypeLibrary.

        """
        self.register(PushType(name, underlying_types, is_collection, is_numeric, coercion_func=coercion_func), force)
        return self

    def unregister(self, push_type_name: str):
        """Unregister a push type by name.

        Parameters
        ----------
        push_type_name
            The name of the push type to unregister.

        Returns
        -------
        PushTypeLibrary
            A reference to the PushTypeLibrary.

        """
        if push_type_name in RESERVED_PSEUDO_STACKS:
            raise ValueError("Cannot unregister PushType with name {nm} because it is reserved.".format(nm=push_type_name))
        self.pop(push_type_name, None)
        return self

    def register_list(self, list_of_push_types: Sequence[PushType]):
        """Register a list of PushType ojbects.

        Parameters
        ----------
        list_of_push_types
            List of Instruction objects to register.

        Returns
        -------
        PushTypeLibrary
            A reference to the PushTypeLibrary.

        """
        for push_type in list_of_push_types:
            self.register(push_type)
        return self

    def register_core(self):
        """Register all core PushTypes defined in pyshgp.

        Returns
        -------
        PushTypeLibrary
            A reference to the PushTypeLibrary.

        """
        for push_type in CORE_PUSH_TYPES:
            self.register(push_type)

    def supported_stacks(self) -> Set[str]:
        """All stack names which the PushTypeLibrary can support.

        Returns
        -------
        set[str]
            A set of stacks names which the type library can support.

        """
        return set(self.keys())

    def push_type_of(self, thing: Any, error_on_not_found: bool = False) -> Optional[PushType]:
        """Return the PushType of the given thing.

        Parameters
        ----------
        thing : Any
            Any value to try and find the corresponding PushType.
        error_on_not_found : bool, optional
            If True, will raise error if no PushType found. Default is False.

        Returns
        -------
        Optional[PushType]
            The corresponding PushType of the thing. If no corresponding type, returns None.

        """
        return self.push_type_for_type(type(thing), error_on_not_found)

    def push_type_for_type(self, typ: type, error_on_not_found: bool = False) -> Optional[PushType]:
        """Return the PushType of the given python (or numpy) type.

        Parameters
        ----------
        typ : type
            Any type to try and find the corresponding PushType.
        error_on_not_found : bool, optional
            If True, will raise error if no PushType found. Default is False.

        Returns
        -------
        Optional[PushType]
            The corresponding PushType of the given type. If no corresponding type, returns None.

        """
        for push_type in self.values():
            if typ in push_type.underlying:
                return push_type
        if error_on_not_found:
            raise PushError.no_type(typ)


def infer_literal(val: Any, type_library: PushTypeLibrary) -> Literal:
    """Make a literal by infering the PushType of the value.

    Parameters
    ----------
    val : Any
        Any value to try and make a Literal out of.
    type_library : PushTypeLibrary
        The library of PushTypes which a Literal can be made of.

    Returns
    -------
    Literal
        The Literal object which holds the value and the corresponding PushType.

    """
    return Literal(value=val, push_type=type_library.push_type_of(val, error_on_not_found=True))
