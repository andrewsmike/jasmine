  WITH RECURSIVE blah AS (SELECT abcd FROM my_table LIMIT 1),
       bleh AS (SELECT 1 FROM taaable)
SELECT *
  FROM foo
 INNER JOIN blah
    ON foo.abcd = blah.abcd;

  WITH RECURSIVE blah AS (
      SELECT abcd, SUM(bleh)
        FROM my_table
       GROUP BY abcd
       ORDER BY abcd DESC
       LIMIT 10
    ),
       bleh AS (SELECT 1 FROM taaable)
SELECT 1;

    WITH RECURSIVE blah AS (
      SELECT abcd, SUM(bleh)
        FROM my_table
       GROUP BY abcd
       ORDER BY 1 DESC
       LIMIT 10
      ),
         bleh AS (
      SELECT abcd, SUM(bleh)
        FROM my_table
       GROUP BY abcd
       ORDER BY 1 ASC
       LIMIT 10
      )
  SELECT 1
    FROM foo
STRAIGHT_JOIN bar
      ON 1;
