from jasmine.etl.materializations.upsert import upsert_event_funcs
from jasmine.etl.materializations.view import view_event_funcs

materialization_event_funcs = {
    "view": view_event_funcs,
    "upsert": upsert_event_funcs,
}
