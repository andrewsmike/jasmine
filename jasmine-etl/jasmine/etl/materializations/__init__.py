from jasmine.etl.materializations.history_table import (
    history_table_event_funcs,
    history_table_resource_names,
)
from jasmine.etl.materializations.incremental import (
    incremental_event_funcs,
    incremental_resource_names,
)
from jasmine.etl.materializations.reload import (
    reload_event_funcs,
    reload_resource_names,
)
from jasmine.etl.materializations.upsert import (
    upsert_event_funcs,
    upsert_resource_names,
)
from jasmine.etl.materializations.view import view_event_funcs, view_resource_names

materialization_event_funcs = {
    "history_table": history_table_event_funcs,
    "incremental": incremental_event_funcs,
    "reload": reload_event_funcs,
    "upsert": upsert_event_funcs,
    "view": view_event_funcs,
}

materialization_resource_names_funcs = {
    "history_table": history_table_resource_names,
    "incremental": incremental_resource_names,
    "view": view_resource_names,
    "upsert": upsert_resource_names,
    "reload": reload_resource_names,
}
