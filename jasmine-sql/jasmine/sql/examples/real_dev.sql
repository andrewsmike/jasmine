SELECT organization.name as Organization,
       CONCAT("[", project.name, "]") as Project,
       `view`.path as Path,
       CAST(AVG(LENGTH(`view`.spec->>"$.query_text")) AS SIGNED) AS `Query length`,
       COUNT(DISTINCT backend_event.backend_event_id) AS Events,
       COUNT(DISTINCT `user`.user_id) AS `Possible users`
  FROM views `view`
  LEFT JOIN projects project
    ON `view`.project_id = project.project_id
  LEFT JOIN backend_events backend_event
    ON `view`.view_id = backend_event.view_id
  LEFT JOIN organizations organization
    ON project.organization_id = organization.organization_id
  LEFT JOIN users `user`
    ON user.organization_id = organization.organization_id
 GROUP BY 1, 2, 3
 ORDER BY 1, 2, 3;


SELECT user_teams.`user`,
       user_teams.org,
       user_teams.teams,
       project.name as project,
       COUNT(DISTINCT `view`.view_id) AS view_count,
       SUM(LENGTH(`view`.spec->>"$.query_text")) AS total_query_size
  FROM (
  SELECT `user`.name as `user`,
         organization.name as org,
         GROUP_CONCAT(team.name) as teams,
         organization.organization_id as org_id
    FROM users `user`
    LEFT JOIN team_memberships team_membership
      ON `user`.user_id = team_membership.user_id
    LEFT JOIN teams team
      ON team_membership.team_id = team.team_id
    LEFT JOIN organizations organization
      ON `user`.organization_id = organization.organization_id
   WHERE `user`.user_id = 1
   GROUP BY 1, 2
     ) user_teams
  LEFT JOIN projects project
    ON project.organization_id = user_teams.org_id
  LEFT JOIN views `view`
    ON `view`.project_id = project.project_id
 GROUP BY 1, 2, 3, 4
 ORDER BY 1, 2, 3, 4;
