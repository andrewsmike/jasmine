SELECT DISTINCT a, b
  FROM abcd l
  LEFT JOIN ljkm mm
    ON l.id = mm.l_id
   AND mm.start_time <= l.timestamp
   AND l.timestamp <= mm.end_time
 ORDER BY a /* bcdefghihuteaouhteoanuhaoeuhetoanunaeohsueaohtnuhaeotnhu */
 LIMIT 10;
