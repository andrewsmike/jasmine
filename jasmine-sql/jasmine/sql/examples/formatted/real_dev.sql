SELECT organization.name AS Organization,
       CONCAT("[", project.name, "]") AS Project,
       view.path AS Path,
       CAST(AVG(LENGTH(view.spec->>"$.query_text")) AS SIGNED) AS `Query length`,
       COUNT(DISTINCT backend_event.backend_event_id) AS Events,
       COUNT(DISTINCT user.user_id) AS `Possible users`
  FROM views view
  LEFT JOIN projects project
    ON view.project_id = project.project_id
  LEFT JOIN backend_events backend_event
    ON view.view_id = backend_event.view_id
  LEFT JOIN organizations organization
    ON project.organization_id = organization.organization_id
  LEFT JOIN users user
    ON user.organization_id = organization.organization_id
 GROUP BY 1, 2, 3
 ORDER BY 1 ASC, 2 ASC, 3 ASC;

