(
  (
    SELECT 1 FROM my_table WHERE my_column = "BLAH"
  )
   UNION
  (
    SELECT 2 FROM my_table WHERE my_column = "BLAH"
  )
)
 UNION
(
  (
    SELECT 4 FROM my_table WHERE my_column = "BLAH"
  )
   UNION
  (
    SELECT 5 FROM my_table WHERE my_column = "BLAH"
  )
);

(
  SELECT 1 FROM my_table WHERE my_column = "BLAH"
)
 UNION
(
  SELECT 2 FROM my_table WHERE my_column = "BLAH"
)
 UNION
(
  SELECT 4 FROM my_table WHERE my_column = "BLAH"
)
 UNION
(
  SELECT 5 FROM my_table WHERE my_column = "BLAH"
);

SELECT 1 FROM a UNION ALL SELECT 2 FROM a;
SELECT 1 FROM a UNION SELECT 2 FROM a;

(
    WITH blah AS (SELECT 3)
  SELECT 1
    FROM a
   WHERE a.bleh < 10
   ORDER BY bleh DESC
   LIMIT 1
)
 UNION
(
  SELECT 2 FROM a
);

SELECT 1 UNION SELECT 1 UNION SELECT 1;
SELECT 1 UNION (SELECT 1 UNION SELECT 1);
(SELECT 1 LIMIT 1) LIMIT 1;
