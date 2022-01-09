"""
Represent and manipulate WHERE clause expressions over primary-key columns.

This is used to represent and manipulate regions of a table, and the three parts of interest are:
- Represent equality, inequality, and other regions.
- Generate the SQL expression to constrain a table to a region.
- Break up a region into multiple parts.

Potentially, we may incorporate trivial transformations in the future (IE, translating between more or less granular date formats)
for dealing with tables with differently-represented, but semantically-identical, formats.
"""
from dataclasses import dataclass
from functools import singledispatch
from typing import Any

from jasmine.sql.transforms.escaping import (
    escaped,
    escaped_table_column_list,
    string_literal_expr,
)

Value = Any


@dataclass
class Region:
    pass


@dataclass
class IntersectionRegion(Region):
    """
    AND clause / intersection between multiple regions.
    Useful for representing the combination of single-value columns and multi-value ones.

    See in_region_expr_intersection for an example.
    """

    subregions: list[Region]


@dataclass
class DiscreteRegion(Region):
    """
    IN clause / enumerated points.

    See in_region_expr_discrete for an example.
    """

    columns: list[str]
    points: list[tuple[Value, ...]]


@dataclass
class RangeRegion(Region):
    """
    Inequality clause.

    See in_region_expr_range for an example.
    """

    column: str
    lower_bound_excl: Value | None = None
    lower_bound_incl: Value | None = None

    upper_bound_incl: Value | None = None
    upper_bound_excl: Value | None = None

    def __post_init__(self):
        assert (self.lower_bound_excl is None) or (
            self.lower_bound_incl is None
        ), "Cannot have two lower bounds."
        assert (self.upper_bound_excl is None) or (
            self.upper_bound_incl is None
        ), "Cannot have two upper bounds."

    def lower_bound_is_incl(self) -> bool:
        return self.lower_bound_incl is not None

    def lower_bound_value(self) -> Value | None:
        return self.lower_bound_incl or self.lower_bound_excl

    def upper_bound_is_incl(self) -> bool:
        return self.upper_bound_incl is not None

    def upper_bound_value(self) -> Value | None:
        return self.upper_bound_incl or self.upper_bound_excl


def value_expr(value: Value) -> str:
    """
    What is a SQL-encoded expression that represents this value?
    >>> print(value_expr(2))
    2
    >>> print(value_expr(2.3))
    2.3

    >>> print(value_expr("Hello world!"))
    'Hello world!'
    >>> print(value_expr("Hello '\\" world!;`"))
    'Hello ''" world!;`'
    """
    match value:
        case float() | int():
            return str(value)

        case str():
            return string_literal_expr(value)

    raise ValueError(f"Unknown value type: {type(value)}")


@singledispatch
def in_region_expr(region: Region, table_name: str):
    raise NotImplementedError(f"Unknown type of Region: {type(region)}")


@in_region_expr.register
def in_region_expr_intersection(region: IntersectionRegion, table_name: str):
    """
    >>> subregion_one = DiscreteRegion(columns=["event_id", "org_name"], points=[(1, "my_org"), (2, "my_other_org")])
    >>> subregion_two = DiscreteRegion(columns=["office_name"], points=[("boston")])

    >>> region = IntersectionRegion([subregion_one, subregion_two])
    >>> print(" WHERE " + in_region_expr(region, "my_table"))
     WHERE ((`my_table`.`event_id` = 1 AND `my_table`.`org_name` = 'my_org')
            OR (`my_table`.`event_id` = 2 AND `my_table`.`org_name` = 'my_other_org'))
       AND ((`my_table`.`office_name` = 'b'))
    """
    return "\n   AND ".join(
        "(" + in_region_expr(subregion, table_name).replace("\n", "\n    ") + ")"
        for subregion in region.subregions
    )


@in_region_expr.register
def in_region_expr_discrete(region: DiscreteRegion, table_alias: str):
    """
    >>> region = DiscreteRegion(columns=["event_id", "org_name"], points=[(1, "my_org"), (2, "my_other_org")])
    >>> print(" WHERE " + in_region_expr(region, "my_table"))
     WHERE (`my_table`.`event_id` = 1 AND `my_table`.`org_name` = 'my_org')
        OR (`my_table`.`event_id` = 2 AND `my_table`.`org_name` = 'my_other_org')

    >>> region = DiscreteRegion(columns=["event_id", "org_name"], points=[(i, "my_org") for i in range(51)])
    >>> print(" WHERE " + in_region_expr(region, "my_table"))
     WHERE (`my_table`.`event_id`, `my_table`.`org_name`) IN ((0, 'my_org'),
          (1, 'my_org'),
          (2, 'my_org'),
    ...
          (49, 'my_org'),
          (50, 'my_org'))
    """
    if len(region.points) < 50:
        return "\n    OR ".join(
            "("
            + " AND ".join(
                f"{escaped(table_alias)}.{escaped(column_name)} = {value_expr(value)}"
                for column_name, value in zip(region.columns, point)
            )
            + ")"
            for point in region.points
        )
    else:
        points_expr = ",\n      ".join(
            "(" + ", ".join(value_expr(value) for value in point) + ")"
            for point in region.points
        )
        return f"({escaped_table_column_list(table_alias, region.columns)}) IN ({points_expr})"


@in_region_expr.register
def in_region_expr_range(region: RangeRegion, table_alias: str):
    """
    >>> region = RangeRegion(column="event_id", lower_bound_incl=4, upper_bound_excl=5)
    >>> print(in_region_expr(region, "my_table"))
    4 <= `my_table`.`event_id` < 5

    >>> region = RangeRegion(column="event_id", upper_bound_incl=5)
    >>> print(in_region_expr(region, "my_table"))
    `my_table`.`event_id` <= 5

    >>> region = RangeRegion(column="event_id", lower_bound_excl=5)
    >>> print(in_region_expr(region, "my_table"))
    5 < `my_table`.`event_id`

    >>> region = RangeRegion(column="event_id")
    >>> print(in_region_expr(region, "my_table"))
    1

    >>> region = RangeRegion(column="event_id", lower_bound_incl=4, lower_bound_excl=5)
    Traceback (most recent call last):
      ...
    AssertionError: Cannot have two lower bounds...
    """
    lb_op = ("<", "<=")[region.lower_bound_is_incl()]
    ub_op = ("<", "<=")[region.upper_bound_is_incl()]

    lb_value = region.lower_bound_value()
    ub_value = region.upper_bound_value()

    if (lb_value is None) and (ub_value is None):
        return "1"

    if lb_value is not None:
        prefix = f"{value_expr(lb_value)} {lb_op} "
    else:
        prefix = ""

    if ub_value is not None:
        suffix = f" {ub_op} {value_expr(ub_value)}"
    else:
        suffix = ""

    return prefix + f"{escaped(table_alias)}.{escaped(region.column)}" + suffix
