SELECT 1 WHERE my_col = 3;
SELECT 3, 1
  FROM blah.my_table a
  LEFT JOIN bleh.my_table_two b
    ON a.meh = b.bleh
 LIMIT 1;
SELECT 3, 1 /* my fav column */
  FROM blah.my_table a
  JOIN bleh.extra_table b
    ON a.id = db.b.a_id
 WHERE a = 4.4 OR b = 3
 GROUP BY a, b, 1
HAVING c
 ORDER BY a
 LIMIT 1;
SELECT * FROM my_table WHERE col = "HI";
