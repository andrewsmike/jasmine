SELECT 1 FROM dual;
SELECT 1 FROM a JOIN b JOIN c USING(l) USING (m);
SELECT *
  FROM users `user`
  LEFT JOIN team_memberships team_membership
  LEFT JOIN teams team
    ON team_membership.team_id = team.team_id
    ON `user`.user_id = team_membership.user_id;
/* TODO: This is incremental / gets improved by the pretty printer. Test it! */
SELECT 1
   FROM my_table a
   JOIN b,
        taableeee,
        tuble
   LEFT JOIN my_other_table b
     ON a.b_id = b.b_id
   JOIN (tub, tab, blah)
  CROSS JOIN blah
   JOIN third_table USING (blah)
  INNER JOIN fourth
   JOIN bleh
   LEFT JOIN meh
     ON meh.a = a.meh_id
NATURAL JOIN blih
  WHERE 1;

