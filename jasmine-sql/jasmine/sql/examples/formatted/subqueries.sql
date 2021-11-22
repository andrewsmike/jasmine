 SELECT (SELECT SUM(cost) FROM a_sub WHERE b.a_id = a_sub.id), 1
   FROM blah.my_table a
  INNER JOIN bleh.extra_table b
     ON a.id = db.b.a_id
   LEFT JOIN (SELECT a, b FROM c INNER JOIN d USING (blah)) l
     ON l.b_id = b.id
NATURAL LEFT JOIN my_table_blah
  WHERE a.a_blah = 4.4 + a.b_blah
    AND b.eai IN (SELECT eai FROM good_eai INNER JOIN l)
  GROUP BY a, b, 1
 HAVING c = "hi\nyo" AND (SELECT 1 WHERE e = 4 LIMIT 1) = 1
  ORDER BY a DESC
  LIMIT 1;

SELECT (
    SELECT a_sub.blahhh, SUM(cost)
      FROM (
          SELECT a, b, c, d AS abcdefgh, SUM(my_columns)
            FROM another_very_interesting_table
        STRAIGHT_JOIN my_other_table
              ON my_column_a = my_column_b
           GROUP BY a, b, c, d
          HAVING a = b AND b = c
           ORDER BY abcdf ASC
           LIMIT 1
         ) a_sub
     WHERE b.a_id = a_sub.id
     GROUP BY 1
     ORDER BY 1 DESC
     ),
       1
  FROM blah.my_table a
 INNER JOIN bleh.extra_table b
    ON a.id = db.b.a_id
  LEFT JOIN (SELECT a, b FROM c INNER JOIN d USING (blah)) l
    ON l.b_id = b.id
 WHERE a.a_blah = 4.4 OR a.b_blah = 3 AND b.eai IN (SELECT eai FROM good_eai)
 GROUP BY a, b, 1
HAVING c
 ORDER BY a ASC
 LIMIT 1;

SELECT (
    SELECT SUM(cost)
      FROM a_sub
     WHERE b.a_id = a_sub.id
     LIMIT 100000000000000000000000000000000
     ) AS a
  FROM blah.my_table a
 INNER JOIN bleh.extra_table b
    ON a.id = db.b.a_id
  LEFT JOIN (
    SELECT a AS b
      FROM c
     INNER JOIN d USING (blah)
     WHERE my_column = "BALTEHU"
     ) l
    ON l.b_id = b.id
 WHERE a.a_blah = 4.4 OR a.b_blah = 3 AND b.eai IN (
    SELECT eai
      FROM good_eai
     WHERE good_eai.blah = "hello world!"
     GROUP BY "abcdefghijklmnop"
    HAVING 1
     )
 GROUP BY a, b, 1
HAVING c
 ORDER BY a ASC
 LIMIT 1;
