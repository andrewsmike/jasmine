/* blah */
SELECT SUM(1) FROM my_table /* Comments should be preserved. */;
SELECT COUNT(DISTINCT organization.organization_id) FROM organizations;

SELECT /* bleeeeh */ GROUP_CONCAT(DISTINCT a, b, c * 4 ORDER BY blah ASC, blih ASC SEPARATOR ", ") OVER (bleh PARTITION BY a, b ORDER BY c ASC, d ASC);

/* UDF stuff: */
SELECT MY_FUNC(a, b); /* blah */ /* bleh */
 /* bcdefghihuteaouhteoanuhaoeuhetoanunaeohsueaohtnuhaeotnhu */
