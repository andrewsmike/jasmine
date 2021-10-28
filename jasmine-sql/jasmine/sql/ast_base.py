"""
Semantic representation of parse trees for query manipulation, analysis, and pretty printing.

ASTs discard irrelevant grammatical constructs / separations and convert everything
to more standard python types.
"""
from abc import ABCMeta, abstractclassmethod
from dataclasses import fields

from jasmine.sql.parser.sql import ParseTree


def ordered_dataclass_children(obj, child_type):
    children = []
    for field in fields(obj.__class__):
        field_value = getattr(obj, field.name, None)
        if field_value is None:
            continue

        if isinstance(field_value, child_type):
            children.append(field_value)

        elif isinstance(field_value, (list, tuple)):
            if all(
                isinstance(field_subvalue, child_type) for field_subvalue in field_value
            ):
                children.extend(field_value)

    return children


class ASTNode(metaclass=ABCMeta):
    """
    A semantic representation of a parse tree.
    """

    @abstractclassmethod
    def from_parse_tree(cls, parse_tree: ParseTree) -> "ASTNode":
        raise NotImplementedError

    def node_type_name(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        """
        Readable string for debugging ASTs.
        """
        children = ordered_dataclass_children(self, ASTNode)

        parts = [self.node_type_name()] + [str(child) for child in children]

        can_abbreviate = (
            len(parts) < 5
            and not any("\n" in part for part in parts)
            and max(len(part) for part in parts) < 80
        )
        if can_abbreviate:
            body = f"{', '.join(parts)}"
        else:
            body = ",\n ".join(part.replace("\n", "\n   ") for part in parts)

        return f"[{body}]"
