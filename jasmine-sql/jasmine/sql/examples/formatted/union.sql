SELECT 1
  FROM a
 UNION ALL
SELECT 2
  FROM a;

SELECT 1
  FROM a
 UNION DISTINCT
SELECT 2
  FROM a;

(SELECT 1
  FROM a)
 UNION
SELECT 2
  FROM a;

((SELECT 1
  FROM a))
 UNION
(SELECT 2
  FROM a);

(((SELECT 1
  FROM a LIMIT 1)))
 UNION
(SELECT 2
  FROM a LIMIT 1);

( WITH blah AS (SELECT 3)
  SELECT 1
    FROM a LIMIT 1
) UNION (
  SELECT 2
    FROM a
      );

  WITH RECURSIVE blah AS (
  SELECT abcd
    FROM my_table
   LIMIT 1
     ),  
       bleh AS (
  SELECT 1
    FROM taaable
     )
SELECT 1;


SELECT 1 UNION SELECT 1 UNION SELECT 1;

SELECT 1 UNION (SELECT 1 UNION SELECT 1);

(SELECT 1 UNION SELECT 1) UNION SELECT 1 LIMIT 1;

(SELECT 1 LIMIT 1) LIMIT 1;


       (
    WITH blah AS (SELECT 1)
  SELECT 1
       )
   UNION
  SELECT 2
    FROM blah
STRAIGHT_JOIN blahp;
