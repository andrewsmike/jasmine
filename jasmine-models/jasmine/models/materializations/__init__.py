from jasmine.models.materializations.base import (
    Materialization,
    StateMachine,
    materialization_types,
)
from jasmine.models.materializations.history_table import HistoryTableMaterialization
from jasmine.models.materializations.view import ViewMaterialization
from jasmine.models.project_models import View

__all__ = [
    "Materialization",
    "StateMachine",
    "materialization_type",
    "materialization_types",
    "new_materialization",
]

materialization_type = {
    "view": ViewMaterialization,
    "history_table": HistoryTableMaterialization,
}


def new_materialization(
    view: View,
    mat_type_name: str,
    config: dict,
    preexisting_mat: Materialization | None = None,
) -> "Materialization":
    assert mat_type_name in materialization_type
    mat_class = materialization_type[mat_type_name]

    assert view.view_type in mat_class.acceptable_view_types

    start_state = mat_class.state_machine_type.start_state
    if preexisting_mat:
        assert isinstance(preexisting_mat, mat_class)

        # I _really_ don't like this, but sqlalchemy doesn't make this particularly easy
        # without deleting / reinserting across two commits.
        preexisting_mat.config = config
        preexisting_mat.state = start_state

        return preexisting_mat
    else:
        return mat_class(
            materialization_type=mat_type_name,
            state=mat_class.state_machine_type.start_state,
            config=config,
            view_id=view.view_id,
        )
