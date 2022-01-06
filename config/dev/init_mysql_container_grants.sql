/* By default, jasmine_web_su does _not_ have the grants it needs for inspection, ETL analysis, working in jasmine_test, etc. */
CREATE DATABASE IF NOT EXISTS jasmine_test;

GRANT ALL ON *.* TO 'jasmine_web_su'@'%' WITH GRANT OPTION;
