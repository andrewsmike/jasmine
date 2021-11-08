 SELECT (SELECT SUM(cost) FROM a_sub WHERE b.a_id = a_sub.id), 1 /* my fav column */
   FROM blah.my_table a
   JOIN bleh.extra_table b
     ON a.id = db.b.a_id
   LEFT JOIN (SELECT a, b FROM c JOIN d USING (blah)) l
     ON l.b_id = b.id
NATURAL LEFT JOIN my_table_blah
  WHERE a.a_blah = 4.4 OR a.b_blah = 3 AND b.eai IN (SELECT eai FROM good_eai JOIN l ON a=b)
  GROUP BY a, b, 1
 having c = "hi\nyo" AND (SELECT 1 WHERE e = 4 LIMIT 1) = 1
  ORDER BY a
  LIMIT 1;
SELECT DISTINCT STRAIGHT_JOIN *
  FROM abcd
 ORDER BY a /* bcdefghihuteaouhteoanuhaoeuhetoanunaeohsueaohtnuhaeotnhu */
 LIMIT 10;
SELECT *
  FROM abcd
 ORDER BY a /* uehaotn */
 LIMIT 10;
SELECT *
  FROM abcd /* uuehtonauhoanuaeotnuhoaenhueoahsnueohuntanauuehaotn */
 ORDER BY a 
 LIMIT 10;
SELECT 4
  FROM abcd
 WHERE i = 4
 UNION
SELECT 1
  FROM abcd /* uuehtonauhoanuaeotnuhoaenhueoahsnueohuntanauuehaotn */
 WHERE i = 3;
SELECT (
    SELECT SUM(cost)
      FROM a_sub
     WHERE b.a_id = a_sub.id
    ), 1 
  FROM blah.my_table a
  JOIN bleh.extra_table b
    ON a.id = db.b.a_id
  LEFT JOIN (SELECT a, b FROM c JOIN d USING (blah)) l
    ON l.b_id = b.id
 WHERE a.a_blah = 4.4 OR a.b_blah = 3 AND b.eai IN (SELECT eai FROM good_eai)
 GROUP BY a, b, 1
having c
 ORDER BY a
 LIMIT 1;
SELECT (
    SELECT SUM ( cost )
      FROM a_sub
     WHERE b.a_id = a_sub.id
     ) 1
  FROM blah.my_table a
  JOIN bleh.extra_table b
    ON a.id = db.b.a_id
  LEFT JOIN (
    SELECT a b
      FROM c
      JOIN d USING ( blah )
     ) l
   ON l.b_id = b.id
 WHERE a.a_blah = 4.4 OR a.b_blah = 3
   AND b.eai IN (
    SELECT eai
      FROM good_eai
     )
 GROUP BY a, b, 1
HAVING c
 ORDER BY a
 LIMIT 1;
