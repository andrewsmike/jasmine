select `user_teams`.`user` AS `user`,`user_teams`.`org` AS `org`,`user_teams`.`teams` AS `teams`,`project`.`name` AS `project`,count(distinct `view`.`view_id`) AS `view_count`,sum(length(json_unquote(json_extract(`view`.`spec`,'$.query_text')))) AS `total_query_size` from (((select `user`.`name` AS `user`,`organization`.`name` AS `org`,group_concat(`team`.`name` separator ',') AS `teams`,`organization`.`organization_id` AS `org_id` from (((`jasmine_test`.`users` `user` left join `jasmine_test`.`team_memberships` `team_membership` on((`user`.`user_id` = `team_membership`.`user_id`))) left join `jasmine_test`.`teams` `team` on((`team_membership`.`team_id` = `team`.`team_id`))) left join `jasmine_test`.`organizations` `organization` on((`user`.`organization_id` = `organization`.`organization_id`))) where (`user`.`user_id` = 1) group by `user`.`name`,`organization`.`name`) `user_teams` left join `jasmine_test`.`projects` `project` on((`project`.`organization_id` = `user_teams`.`org_id`))) left join `jasmine_test`.`views` `view` on((`view`.`project_id` = `project`.`project_id`))) group by `user_teams`.`user`,`user_teams`.`org`,`user_teams`.`teams`,`project`.`name` order by `user_teams`.`user`,`user_teams`.`org`,`user_teams`.`teams`,`project`.`name`;