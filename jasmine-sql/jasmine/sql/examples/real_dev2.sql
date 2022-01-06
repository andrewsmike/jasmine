SELECT backend_event_id AS event_id,
       CONCAT(organization.name, ": ", backend.name, ":[", project.name, "]/", view.path) AS path,
       CONCAT(materialization.materialization_type, " materialized ", view.view_type) AS method
       materialization.state,
       materialization.config,
       materialization.context,
       description,
       reason,
       created_time AS updated_ts
  FROM jasmine_web.backend_events backend_event
  LEFT JOIN materializations materialization
    ON materialization.materialization_id = backend_event.materialization_id
  LEFT JOIN views view
    ON view.view_id = backend_event.view_id
  LEFT JOIN projects project
    ON projects.project_id = backend_event.project_id
  LEFT JOIN backends backend
    ON backends.backend_id = backend_event.backend_id
  LEFT JOIN organizations organization
    ON organization.organization_id = backend.organization_id
 ORDER BY event_id ASC;
