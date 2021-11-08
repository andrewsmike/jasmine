SELECT SUM(1) FROM my_table;
SELECT COUNT(DISTINCT organization.organization_id) FROM organizations;
SELECT GROUP_CONCAT(DISTINCT a, b, c * 4 ORDER BY blah, blih SEPARATOR ", ") OVER (bleh PARTITION BY a, b ORDER BY c, d );
/* UDF stuff: */
SELECT MY_FUNC(a, b); /* blah */
