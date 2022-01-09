from jasmine.etl.materializations.upsert import (
    upsert_event_funcs,
    upsert_resource_names,
)
from jasmine.etl.materializations.view import view_event_funcs, view_resource_names

materialization_event_funcs = {
    "view": view_event_funcs,
    "upsert": upsert_event_funcs,
}

materialization_resource_names_funcs = {
    "view": view_resource_names,
    "upsert": upsert_resource_names,
}
