-- MySQL dump 10.13  Distrib 8.0.26-16, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: jasmine_web
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*!50717 SELECT COUNT(*) INTO @rocksdb_has_p_s_session_variables FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'performance_schema' AND TABLE_NAME = 'session_variables' */;
/*!50717 SET @rocksdb_get_is_supported = IF (@rocksdb_has_p_s_session_variables, 'SELECT COUNT(*) INTO @rocksdb_is_supported FROM performance_schema.session_variables WHERE VARIABLE_NAME=\'rocksdb_bulk_load\'', 'SELECT 0') */;
/*!50717 PREPARE s FROM @rocksdb_get_is_supported */;
/*!50717 EXECUTE s */;
/*!50717 DEALLOCATE PREPARE s */;
/*!50717 SET @rocksdb_enable_bulk_load = IF (@rocksdb_is_supported, 'SET SESSION rocksdb_bulk_load = 1', 'SET @rocksdb_dummy_bulk_load = 0') */;
/*!50717 PREPARE s FROM @rocksdb_enable_bulk_load */;
/*!50717 EXECUTE s */;
/*!50717 DEALLOCATE PREPARE s */;

--
-- Current Database: `jasmine_web`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `jasmine_web` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `jasmine_web`;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('1a665a343d3e');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `analytics/user_project_facts_from_view_view`
--

DROP TABLE IF EXISTS `analytics/user_project_facts_from_view_view`;
/*!50001 DROP VIEW IF EXISTS `analytics/user_project_facts_from_view_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `analytics/user_project_facts_from_view_view` AS SELECT 
 1 AS `user`,
 1 AS `org`,
 1 AS `teams`,
 1 AS `project`,
 1 AS `view_count`,
 1 AS `total_query_size`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `analytics/user_project_facts_view`
--

DROP TABLE IF EXISTS `analytics/user_project_facts_view`;
/*!50001 DROP VIEW IF EXISTS `analytics/user_project_facts_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `analytics/user_project_facts_view` AS SELECT 
 1 AS `user`,
 1 AS `org`,
 1 AS `teams`,
 1 AS `project`,
 1 AS `view_count`,
 1 AS `total_query_size`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `analytics/user_view_facts_view`
--

DROP TABLE IF EXISTS `analytics/user_view_facts_view`;
/*!50001 DROP VIEW IF EXISTS `analytics/user_view_facts_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `analytics/user_view_facts_view` AS SELECT 
 1 AS `Organization`,
 1 AS `Project`,
 1 AS `Path`,
 1 AS `Query length`,
 1 AS `Events`,
 1 AS `Possible users`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `backend_events`
--

DROP TABLE IF EXISTS `backend_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backend_events` (
  `backend_event_id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `description` text,
  `created_time` datetime NOT NULL,
  `materialization_id` bigint DEFAULT NULL,
  `view_id` bigint DEFAULT NULL,
  `project_id` bigint DEFAULT NULL,
  `backend_id` bigint NOT NULL,
  PRIMARY KEY (`backend_event_id`),
  KEY `backend_event_backend` (`backend_id`),
  KEY `project_event_view` (`project_id`),
  KEY `backend_event_view` (`view_id`),
  KEY `created_time` (`created_time`),
  KEY `backend_event_materialization` (`materialization_id`),
  CONSTRAINT `backend_event_backend` FOREIGN KEY (`backend_id`) REFERENCES `backends` (`backend_id`),
  CONSTRAINT `backend_event_materialization` FOREIGN KEY (`materialization_id`) REFERENCES `materializations` (`materialization_id`),
  CONSTRAINT `backend_event_view` FOREIGN KEY (`view_id`) REFERENCES `views` (`view_id`),
  CONSTRAINT `project_event_view` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backend_events`
--

LOCK TABLES `backend_events` WRITE;
/*!40000 ALTER TABLE `backend_events` DISABLE KEYS */;
INSERT INTO `backend_events` VALUES (1,'Created backend blahblah with view','blahblah','2021-09-29 04:54:52',NULL,1,1,1),(2,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 21:15:50',1,1,1,1),(3,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 21:16:07',1,1,1,1),(4,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 21:16:13',1,1,1,1),(5,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 21:17:19',1,1,1,1),(6,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 22:17:32',1,1,1,1),(7,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 22:18:31',1,1,1,1),(8,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 22:20:19',1,1,1,1),(9,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 22:21:15',1,1,1,1),(10,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 22:27:47',1,1,1,1),(11,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 22:28:03',1,1,1,1),(12,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 22:34:43',1,1,1,1),(13,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 22:40:24',1,1,1,1),(14,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 23:05:30',1,1,1,1),(15,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty()\nAssertionError\n','2021-12-29 23:17:21',1,1,1,1),(16,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: ResourceNames(tables=set(), views={(\'jasmine_test\', \'analytics/user_project_facts_view\')}, triggers=set())\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 72, in terminate_view\n    assert resources.empty(), str(resources)\nAssertionError: ResourceNames(tables=set(), views={(\'jasmine_test\', \'analytics/user_project_facts_view\')}, triggers=set())\n','2021-12-29 23:30:53',1,1,1,1),(17,'Materialization event failed','Failed to run; Entering bad_spec.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 62, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 18:33:38',NULL,NULL,1,1),(18,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:07:16',NULL,NULL,1,1),(19,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:07:55',NULL,NULL,1,1),(20,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:13:20',NULL,NULL,1,1),(21,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:13:25',NULL,NULL,1,1),(22,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:13:37',NULL,NULL,1,1),(23,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1146, \"Table \'jasmine_web.my_dataset\' doesn\'t exist\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.ProgrammingError: (1146, \"Table \'jasmine_web.my_dataset\' doesn\'t exist\")\n','2021-12-30 19:13:52',NULL,NULL,1,1),(24,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:14:49',NULL,NULL,1,1),(25,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:41:29',NULL,NULL,1,1),(26,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1054, \"Unknown column \'1tuheoan\' in \'field list\'\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.OperationalError: (1054, \"Unknown column \'1tuheoan\' in \'field list\'\")\n','2021-12-30 19:41:33',NULL,NULL,1,1),(27,'Materialization event failed','Failed to run; Entering could_not_terminate.\nReason: name \'debug\' is not defined\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 69, in terminate_view\n    conn.execute(drop_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 27, in execute\n    if debug:\nNameError: name \'debug\' is not defined\n','2021-12-30 19:48:10',NULL,NULL,1,1),(28,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:50:41',NULL,NULL,1,1),(29,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2021-12-30 19:54:31',NULL,NULL,1,1),(30,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2022-01-05 17:11:46',16,51,1,1),(31,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1305, \'FUNCTION jasmine_web.STRING_CONCAT does not exist\')\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.OperationalError: (1305, \'FUNCTION jasmine_web.STRING_CONCAT does not exist\')\n','2022-01-05 17:18:04',16,51,1,1),(32,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1305, \'FUNCTION jasmine_web.STRING_CONCAT does not exist\')\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.OperationalError: (1305, \'FUNCTION jasmine_web.STRING_CONCAT does not exist\')\n','2022-01-05 17:18:04',16,51,1,1),(33,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2022-01-05 17:20:42',16,51,1,1),(34,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1054, \"Unknown column \'reason\' in \'field list\'\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.OperationalError: (1054, \"Unknown column \'reason\' in \'field list\'\")\n','2022-01-05 17:21:56',16,51,1,1),(35,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2022-01-05 17:24:37',16,51,1,1),(36,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2022-01-05 17:24:37',16,51,1,1),(37,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1054, \"Unknown column \'backend_event_id\' in \'field list\'\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.OperationalError: (1054, \"Unknown column \'backend_event_id\' in \'field list\'\")\n','2022-01-05 17:26:29',16,51,1,1),(38,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1054, \"Unknown column \'reason\' in \'field list\'\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.OperationalError: (1054, \"Unknown column \'reason\' in \'field list\'\")\n','2022-01-05 17:26:36',16,51,1,1),(39,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2022-01-05 17:26:42',16,51,1,1),(40,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1054, \"Unknown column \'reason\' in \'field list\'\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.OperationalError: (1054, \"Unknown column \'reason\' in \'field list\'\")\n','2022-01-05 17:27:39',16,51,1,1),(41,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1054, \"Unknown column \'backends.backend_id\' in \'on clause\'\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.OperationalError: (1054, \"Unknown column \'backends.backend_id\' in \'on clause\'\")\n','2022-01-05 17:28:07',16,51,1,1),(42,'Materialization event failed','Failed to run; Entering rejected.\nReason: \nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\nAssertionError\n','2022-01-07 01:09:38',17,52,1,1),(43,'Materialization event failed','Failed to run; Entering rejected.\nReason: At 3:10: no viable alternative at input \'SELECT *\\n  FROM jasmine_web.incremental_demo_upsert\\n ORDER BY \'\nTraceback (most recent call last):\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 21056, in selectStatement\n    la_ = self._interp.adaptivePredict(self._input,279,self._ctx)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/atn/ParserATNSimulator.py\", line 346, in adaptivePredict\n    alt = self.execATN(dfa, s0, input, index, outerContext)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/atn/ParserATNSimulator.py\", line 418, in execATN\n    raise e\nantlr4.error.Errors.NoViableAltException: None\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\n  File \"/opt/jasmine-sql/jasmine/sql/analysis.py\", line 70, in is_readonly_query\n    sql_program = sql_tree_from_str(query)\n  File \"/opt/jasmine-sql/jasmine/sql/parser/sql.py\", line 85, in sql_tree_from_str\n    return sql_tree_from_stream(InputStream(query))\n  File \"/opt/jasmine-sql/jasmine/sql/parser/sql.py\", line 75, in sql_tree_from_stream\n    program = parser.sqlProgram()\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 7618, in sqlProgram\n    self.statement()\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 7700, in statement\n    self.simpleStatement()\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 7959, in simpleStatement\n    self.selectStatement()\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 21086, in selectStatement\n    self._errHandler.reportError(self, re)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/error/ErrorStrategy.py\", line 126, in reportError\n    self.reportNoViableAlternative(recognizer, e)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/error/ErrorStrategy.py\", line 261, in reportNoViableAlternative\n    recognizer.notifyErrorListeners(msg, e.offendingToken, e)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/Parser.py\", line 322, in notifyErrorListeners\n    listener.syntaxError(self, offendingToken, line, column, msg, e)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/error/ErrorListener.py\", line 60, in syntaxError\n    delegate.syntaxError(recognizer, offendingSymbol, line, column, msg, e)\n  File \"/opt/jasmine-sql/jasmine/sql/parser/sql.py\", line 24, in syntaxError\n    raise SyntaxError(f\"At {line}:{column}: {msg}\")\nSyntaxError: At 3:10: no viable alternative at input \'SELECT *\\n  FROM jasmine_web.incremental_demo_upsert\\n ORDER BY \'\n','2022-01-07 01:13:58',17,52,1,1),(44,'Materialization event failed','Failed to run; Entering rejected.\nReason: At 3:10: no viable alternative at input \'SELECT *\\n  FROM jasmine_web.incremental_demo_upsert\\n ORDER BY \'\nTraceback (most recent call last):\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 21056, in selectStatement\n    la_ = self._interp.adaptivePredict(self._input,279,self._ctx)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/atn/ParserATNSimulator.py\", line 346, in adaptivePredict\n    alt = self.execATN(dfa, s0, input, index, outerContext)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/atn/ParserATNSimulator.py\", line 418, in execATN\n    raise e\nantlr4.error.Errors.NoViableAltException: None\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 32, in verify_view\n    assert is_readonly_query(view_sql)\n  File \"/opt/jasmine-sql/jasmine/sql/analysis.py\", line 70, in is_readonly_query\n    sql_program = sql_tree_from_str(query)\n  File \"/opt/jasmine-sql/jasmine/sql/parser/sql.py\", line 85, in sql_tree_from_str\n    return sql_tree_from_stream(InputStream(query))\n  File \"/opt/jasmine-sql/jasmine/sql/parser/sql.py\", line 75, in sql_tree_from_stream\n    program = parser.sqlProgram()\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 7618, in sqlProgram\n    self.statement()\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 7700, in statement\n    self.simpleStatement()\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 7959, in simpleStatement\n    self.selectStatement()\n  File \"/opt/jasmine-sql/jasmine/sql/parser/SQLParser.py\", line 21086, in selectStatement\n    self._errHandler.reportError(self, re)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/error/ErrorStrategy.py\", line 126, in reportError\n    self.reportNoViableAlternative(recognizer, e)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/error/ErrorStrategy.py\", line 261, in reportNoViableAlternative\n    recognizer.notifyErrorListeners(msg, e.offendingToken, e)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/Parser.py\", line 322, in notifyErrorListeners\n    listener.syntaxError(self, offendingToken, line, column, msg, e)\n  File \"/usr/local/lib/python3.10/site-packages/antlr4/error/ErrorListener.py\", line 60, in syntaxError\n    delegate.syntaxError(recognizer, offendingSymbol, line, column, msg, e)\n  File \"/opt/jasmine-sql/jasmine/sql/parser/sql.py\", line 24, in syntaxError\n    raise SyntaxError(f\"At {line}:{column}: {msg}\")\nSyntaxError: At 3:10: no viable alternative at input \'SELECT *\\n  FROM jasmine_web.incremental_demo_upsert\\n ORDER BY \'\n','2022-01-07 01:13:58',17,52,1,1),(45,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1146, \"Table \'jasmine_web.incremental_demo_upsert\' doesn\'t exist\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.ProgrammingError: (1146, \"Table \'jasmine_web.incremental_demo_upsert\' doesn\'t exist\")\n','2022-01-07 01:14:23',17,52,1,1),(46,'Materialization event failed','Failed to run; Entering could_not_create.\nReason: (1146, \"Table \'jasmine_test.incremental_demo_upsert\' doesn\'t exist\")\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/view.py\", line 48, in create_view\n    conn.execute(create_view_sql)\n  File \"/opt/jasmine-etl/jasmine/etl/backends.py\", line 36, in execute\n    return super().execute(context_str + query, args=args)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 148, in execute\n    result = self._query(query)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/cursors.py\", line 310, in _query\n    conn.query(q)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 548, in query\n    self._affected_rows = self._read_query_result(unbuffered=unbuffered)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 775, in _read_query_result\n    result.read()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 1156, in read\n    first_packet = self.connection._read_packet()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/connections.py\", line 725, in _read_packet\n    packet.raise_for_error()\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/protocol.py\", line 221, in raise_for_error\n    err.raise_mysql_exception(self._data)\n  File \"/usr/local/lib/python3.10/site-packages/pymysql/err.py\", line 143, in raise_mysql_exception\n    raise errorclass(errno, errval)\npymysql.err.ProgrammingError: (1146, \"Table \'jasmine_test.incremental_demo_upsert\' doesn\'t exist\")\n','2022-01-07 01:50:21',17,52,1,1),(47,'Materialization event failed','Failed to run; Entering rejected.\nReason: The UPSERT materialization requires at least one primary or unique key.\nTraceback (most recent call last):\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/etl_tools.py\", line 65, in wrapped\n    return func(materialization, session, *args, **kwargs)\n  File \"/opt/jasmine-etl/jasmine/etl/materializations/upsert.py\", line 80, in verify_upsert\n    assert self.config.get(\nAssertionError: The UPSERT materialization requires at least one primary or unique key.\n','2022-01-09 00:26:16',18,51,1,1);
/*!40000 ALTER TABLE `backend_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backends`
--

DROP TABLE IF EXISTS `backends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backends` (
  `backend_id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `backend_type` enum('mysql') NOT NULL,
  `spec` json NOT NULL,
  `organization_id` bigint NOT NULL,
  PRIMARY KEY (`backend_id`),
  UNIQUE KEY `organization_id` (`organization_id`,`name`),
  CONSTRAINT `backend_organization` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backends`
--

LOCK TABLES `backends` WRITE;
/*!40000 ALTER TABLE `backends` DISABLE KEYS */;
INSERT INTO `backends` VALUES (1,'jasmine-web','mysql','{\"connection_args\": {\"host\": \"database\", \"port\": 3306, \"user\": \"jasmine_web_su\", \"database\": \"jasmine_web\", \"password\": \"password\"}}',1);
/*!40000 ALTER TABLE `backends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `incremental_demo_from_upsert_view`
--

DROP TABLE IF EXISTS `incremental_demo_from_upsert_view`;
/*!50001 DROP VIEW IF EXISTS `incremental_demo_from_upsert_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `incremental_demo_from_upsert_view` AS SELECT 
 1 AS `jsmn_auto_id`,
 1 AS `event_id`,
 1 AS `path`,
 1 AS `method`,
 1 AS `state`,
 1 AS `config`,
 1 AS `context`,
 1 AS `title`,
 1 AS `description`,
 1 AS `updated_ts`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `incremental_demo_upsert`
--

DROP TABLE IF EXISTS `incremental_demo_upsert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incremental_demo_upsert` (
  `jsmn_auto_id` bigint NOT NULL AUTO_INCREMENT,
  `event_id` bigint NOT NULL,
  `path` varchar(256) DEFAULT NULL,
  `method` varchar(64) DEFAULT NULL,
  `state` varchar(64) DEFAULT NULL,
  `config` text,
  `context` text,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `updated_ts` datetime DEFAULT NULL,
  PRIMARY KEY (`jsmn_auto_id`),
  UNIQUE KEY `event_id` (`event_id`),
  KEY `_jsmn_key_0` (`description`),
  KEY `_jsmn_key_1` (`event_id`),
  KEY `_jsmn_key_2` (`path`),
  KEY `_jsmn_key_3` (`title`,`description`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incremental_demo_upsert`
--

LOCK TABLES `incremental_demo_upsert` WRITE;
/*!40000 ALTER TABLE `incremental_demo_upsert` DISABLE KEYS */;
INSERT INTO `incremental_demo_upsert` VALUES (1,47,'My Company:jasmine-web:[dev]/incremental_demo','upsert materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"table_spec\": {\"indices\": {\"_jsmn_key_0\": [\"description\"], \"_jsmn_key_1\": [\"event_id\"], \"_jsmn_key_2\": [\"path\"], \"_jsmn_key_3\": [\"title\", \"description\"]}, \"primary_key\": [\"jsmn_auto_id\"], \"column_names\": [\"jsmn_auto_id\", \"event_id\", \"path\", \"method\", \"state\", \"config\", \"context\", \"title\", \"description\", \"updated_ts\"], \"foreign_keys\": [], \"unique_indices\": {\"event_id\": [\"event_id\"]}, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\", \"jsmn_auto_id\": \"BIGINT NOT NULL AUTO_INCREMENT\"}}, \"high_water_mark\": 1641688740.641607, \"claimed_resources\": {\"views\": [], \"tables\": [[\"jasmine_web\", \"incremental_demo_upsert\"]], \"triggers\": []}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-09 00:26:16'),(2,46,'My Company:jasmine-web:[dev]/incremental_demo_from_upsert','view materialized query','could_not_create','{}','{\"claimed_resources\": {}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-07 01:50:21'),(3,45,'My Company:jasmine-web:[dev]/incremental_demo_from_upsert','view materialized query','could_not_create','{}','{\"claimed_resources\": {}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-07 01:14:23'),(4,44,'My Company:jasmine-web:[dev]/incremental_demo_from_upsert','view materialized query','could_not_create','{}','{\"claimed_resources\": {}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-07 01:13:58'),(5,43,'My Company:jasmine-web:[dev]/incremental_demo_from_upsert','view materialized query','could_not_create','{}','{\"claimed_resources\": {}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-07 01:13:58'),(6,42,'My Company:jasmine-web:[dev]/incremental_demo_from_upsert','view materialized query','could_not_create','{}','{\"claimed_resources\": {}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-07 01:09:38'),(7,41,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-05 17:28:07'),(8,40,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-05 17:27:39'),(9,39,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-05 17:26:42'),(10,38,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-05 17:26:36'),(11,37,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-05 17:26:29'),(12,36,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-05 17:24:37'),(13,35,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-05 17:24:37'),(14,34,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-05 17:21:56'),(15,33,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-05 17:20:42'),(16,32,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-05 17:18:04'),(17,31,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_create.','2022-01-05 17:18:04'),(18,30,'My Company:jasmine-web:[dev]/incremental_demo','view materialized query','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering rejected.','2022-01-05 17:11:46'),(19,29,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:54:31'),(20,28,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:50:41'),(21,27,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-30 19:48:10'),(22,26,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering could_not_create.','2021-12-30 19:41:33'),(23,25,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:41:29'),(24,24,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:14:49'),(25,23,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering could_not_create.','2021-12-30 19:13:52'),(26,22,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:13:37'),(27,21,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:13:25'),(28,20,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:13:20'),(29,19,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:07:55'),(30,18,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering rejected.','2021-12-30 19:07:16'),(31,17,'My Company:jasmine-web:[dev]/',NULL,NULL,NULL,NULL,'Materialization event failed','Failed to run; Entering bad_spec.','2021-12-30 18:33:38'),(32,16,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 23:30:53'),(33,15,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 23:17:21'),(34,14,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 23:05:30'),(35,13,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 22:40:24'),(36,12,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 22:34:43'),(37,11,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 22:28:03'),(38,10,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 22:27:47'),(39,9,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 22:21:15'),(40,8,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 22:20:19'),(41,7,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 22:18:31'),(42,6,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 22:17:32'),(43,5,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 21:17:19'),(44,4,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 21:16:13'),(45,3,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 21:16:07'),(46,2,'My Company:jasmine-web:[dev]/analytics/user_project_facts','view materialized query','active','{}','{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}','Materialization event failed','Failed to run; Entering could_not_terminate.','2021-12-29 21:15:50');
/*!40000 ALTER TABLE `incremental_demo_upsert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `incremental_demo_view`
--

DROP TABLE IF EXISTS `incremental_demo_view`;
/*!50001 DROP VIEW IF EXISTS `incremental_demo_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `incremental_demo_view` AS SELECT 
 1 AS `event_id`,
 1 AS `path`,
 1 AS `method`,
 1 AS `state`,
 1 AS `config`,
 1 AS `context`,
 1 AS `title`,
 1 AS `description`,
 1 AS `updated_ts`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `materializations`
--

DROP TABLE IF EXISTS `materializations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materializations` (
  `materialization_id` bigint NOT NULL AUTO_INCREMENT,
  `materialization_type` enum('view','history_table','upsert','reload') NOT NULL,
  `state` varchar(64) NOT NULL,
  `config` json NOT NULL,
  `view_id` bigint NOT NULL,
  `context` json NOT NULL,
  PRIMARY KEY (`materialization_id`),
  UNIQUE KEY `view_id` (`view_id`,`materialization_type`),
  CONSTRAINT `materializations_ibfk_1` FOREIGN KEY (`view_id`) REFERENCES `views` (`view_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materializations`
--

LOCK TABLES `materializations` WRITE;
/*!40000 ALTER TABLE `materializations` DISABLE KEYS */;
INSERT INTO `materializations` VALUES (1,'view','active','{}',1,'{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_view\"]], \"tables\": [], \"triggers\": []}}'),(7,'view','terminated','{}',2,'{\"claimed_resources\": {}}'),(9,'view','active','{}',28,'{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_view_facts_view\"]], \"tables\": [], \"triggers\": []}}'),(10,'view','active','{}',43,'{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"analytics/user_project_facts_from_view_view\"]], \"tables\": [], \"triggers\": []}}'),(16,'view','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}',51,'{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_view\"]], \"tables\": [], \"triggers\": []}}'),(17,'view','active','{}',52,'{\"claimed_resources\": {\"views\": [[\"jasmine_web\", \"incremental_demo_from_upsert_view\"]], \"tables\": [], \"triggers\": []}}'),(18,'upsert','active','{\"keys\": {\"path\": [\"path\"], \"title\": [\"title\"], \"title2\": [\"title\", \"description\"], \"event_id\": [\"event_id\"], \"description\": [\"description\"]}, \"unique_keys\": {\"event_id\": [\"event_id\"]}, \"start_timestamp\": 1636499182, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\"}, \"updated_ts_column_name\": \"updated_ts\"}',51,'{\"table_spec\": {\"indices\": {\"_jsmn_key_0\": [\"description\"], \"_jsmn_key_1\": [\"event_id\"], \"_jsmn_key_2\": [\"path\"], \"_jsmn_key_3\": [\"title\", \"description\"]}, \"primary_key\": [\"jsmn_auto_id\"], \"column_names\": [\"jsmn_auto_id\", \"event_id\", \"path\", \"method\", \"state\", \"config\", \"context\", \"title\", \"description\", \"updated_ts\"], \"foreign_keys\": [], \"unique_indices\": {\"event_id\": [\"event_id\"]}, \"column_type_decls\": {\"path\": \"VARCHAR(256)\", \"state\": \"VARCHAR(64)\", \"title\": \"VARCHAR(255)\", \"config\": \"TEXT\", \"method\": \"VARCHAR(64)\", \"context\": \"TEXT\", \"event_id\": \"BIGINT NOT NULL\", \"updated_ts\": \"DATETIME\", \"description\": \"VARCHAR(255)\", \"jsmn_auto_id\": \"BIGINT NOT NULL AUTO_INCREMENT\"}}, \"high_water_mark\": 1641688821.382447, \"claimed_resources\": {\"views\": [], \"tables\": [[\"jasmine_web\", \"incremental_demo_upsert\"]], \"triggers\": []}}');
/*!40000 ALTER TABLE `materializations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizations`
--

DROP TABLE IF EXISTS `organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizations` (
  `organization_id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`organization_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizations`
--

LOCK TABLES `organizations` WRITE;
/*!40000 ALTER TABLE `organizations` DISABLE KEYS */;
INSERT INTO `organizations` VALUES (1,'My Company');
/*!40000 ALTER TABLE `organizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `project_id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `backend_id` bigint NOT NULL,
  `organization_id` bigint NOT NULL,
  PRIMARY KEY (`project_id`),
  UNIQUE KEY `organization_id` (`organization_id`,`name`),
  KEY `backend` (`backend_id`),
  CONSTRAINT `project_backend` FOREIGN KEY (`backend_id`) REFERENCES `backends` (`backend_id`),
  CONSTRAINT `project_organization` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'dev',1,1);
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_memberships`
--

DROP TABLE IF EXISTS `team_memberships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team_memberships` (
  `team_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`team_id`,`user_id`),
  KEY `user_teams` (`user_id`),
  CONSTRAINT `membership_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`),
  CONSTRAINT `membership_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_memberships`
--

LOCK TABLES `team_memberships` WRITE;
/*!40000 ALTER TABLE `team_memberships` DISABLE KEYS */;
INSERT INTO `team_memberships` VALUES (1,1);
/*!40000 ALTER TABLE `team_memberships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `team_id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `organization_id` bigint NOT NULL,
  PRIMARY KEY (`team_id`),
  KEY `org_team_name` (`organization_id`,`name`),
  KEY `team_name` (`name`),
  CONSTRAINT `team_organization` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (1,'data_eng',1);
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(96) NOT NULL,
  `name` varchar(96) NOT NULL,
  `default_project_id` bigint DEFAULT NULL,
  `organization_id` bigint NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  KEY `org_email` (`organization_id`,`email`),
  KEY `org_name` (`organization_id`,`name`),
  KEY `user_default_project` (`default_project_id`),
  CONSTRAINT `user_default_project` FOREIGN KEY (`default_project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `user_organization` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'andrewsm13@gmail.com','Mike Andrews',1,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `views`
--

DROP TABLE IF EXISTS `views`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `views` (
  `view_id` bigint NOT NULL AUTO_INCREMENT,
  `view_type` enum('query') NOT NULL,
  `spec` json NOT NULL,
  `path` varchar(256) NOT NULL,
  `project_id` bigint NOT NULL,
  PRIMARY KEY (`view_id`),
  UNIQUE KEY `project_id` (`project_id`,`path`),
  CONSTRAINT `views_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `views`
--

LOCK TABLES `views` WRITE;
/*!40000 ALTER TABLE `views` DISABLE KEYS */;
INSERT INTO `views` VALUES (1,'query','{\"view_type\": \"query\", \"query_text\": \"/* My Comment */\\nSELECT user_teams.user,\\n       user_teams.org,\\n       user_teams.teams,\\n       project.name AS project,\\n       COUNT(DISTINCT view.view_id) AS view_count,\\n       SUM(LENGTH(view.spec->>\\\"$.query_text\\\")) AS total_query_size\\n  FROM (\\n    SELECT user.name AS user,\\n           organization.name AS org,\\n           GROUP_CONCAT(team.name) AS teams,\\n           organization.organization_id AS org_id\\n      FROM users user\\n      LEFT JOIN team_memberships team_membership\\n        ON user.user_id = team_membership.user_id\\n      LEFT JOIN teams team\\n        ON team_membership.team_id = team.team_id\\n      LEFT JOIN organizations organization\\n        ON user.organization_id = organization.organization_id\\n     WHERE user.user_id = 1\\n     GROUP BY 1, 2\\n     ) user_teams\\n  LEFT JOIN projects project\\n    ON project.organization_id = user_teams.org_id\\n  LEFT JOIN views view\\n    ON view.project_id = project.project_id\\n GROUP BY 1, 2, 3, 4\\n ORDER BY 1 ASC, 2 ASC, 3 ASC, 4 ASC;\"}','analytics/user_project_facts',1),(2,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT *  /* BLAHHHH*/\\n  FROM my_table a  /* BLAH  ueathnu*/\\n  LEFT JOIN my_other_table b\\n    ON a.other_table_id = b.id\\n GROUP BY 1, 2\\n LIMIT 1;\"}','trivial/nonsense',1),(28,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT organization.name as Organization,\\n       CONCAT(\\\"[\\\", project.name, \\\"]\\\") as Project,\\n       `view`.path as Path,\\n       CAST(AVG(LENGTH(`view`.spec->>\\\"$.query_text\\\")) AS SIGNED) AS `Query length`,\\n       COUNT(DISTINCT backend_event.backend_event_id) AS Events,\\n       COUNT(DISTINCT `user`.user_id) AS `Possible users`\\n  FROM views `view`\\n  LEFT JOIN projects project\\n    ON `view`.project_id = project.project_id\\n  LEFT JOIN backend_events backend_event\\n    ON `view`.view_id = backend_event.view_id\\n  LEFT JOIN organizations organization\\n    ON project.organization_id = organization.organization_id\\n  LEFT JOIN users `user`\\n    ON user.organization_id = organization.organization_id\\n GROUP BY 1, 2, 3\\n ORDER BY 1, 2, 3;\\n \"}','analytics/user_view_facts',1),(34,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT 1 AS result\\n  FROM DUAL\\n WHERE 3 > 2\\n LIMIT 1;\"}','trivial/dual',1),(39,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT 1 LIMIT 1;\"}','trivial/limit 1',1),(40,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT *\\n  FROM jasmine_test.views\\n LIMIT 10;\"}','raw/views',1),(42,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT *\\n  FROM users `user`\\n  LEFT JOIN team_memberships team_membership\\n  LEFT JOIN teams team\\n    ON team_membership.team_id = team.team_id\\n    ON `user`.user_id = team_membership.user_id;\\n\"}','trivial/horror_show',1),(43,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT * FROM `analytics/user_project_facts_view`\"}','analytics/user_project_facts_from_view',1),(44,'query','{\"view_type\": \"query\", \"query_text\": \"/* Base query is `analytics.user_view_facts`:\\nSELECT organization.name as Organization,\\n       CONCAT(\\\"[\\\", project.name, \\\"]\\\") as Project,\\n       `view`.path as Path,\\n       CAST(AVG(LENGTH(`view`.spec->>\\\"$.query_text\\\")) AS SIGNED) AS `Query length`,\\n       COUNT(DISTINCT backend_event.backend_event_id) AS Events,\\n       COUNT(DISTINCT `user`.user_id) AS `Possible users`\\n  FROM views `view`\\n  LEFT JOIN projects project\\n    ON `view`.project_id = project.project_id\\n  LEFT JOIN backend_events backend_event\\n    ON `view`.view_id = backend_event.view_id\\n  LEFT JOIN organizations organization\\n    ON project.organization_id = organization.organization_id\\n  LEFT JOIN users `user`\\n    ON user.organization_id = organization.organization_id\\n GROUP BY 1, 2, 3\\n ORDER BY 1, 2, 3;\\n  */\\n/* Operations:\\n * - Delete non-workunit columns\\n * - Aggregate workunit columns as necessary\\n * - Add DISTINCT, remove GROUP BY clause\\n * - Add ORDER BY ASC, remove old ORDER BY clause\\n */\\nSELECT DISTINCT organization.name as Organization,\\n       CONCAT(\\\"[\\\", project.name, \\\"]\\\") as Project,\\n       `view`.path as Path,\\n  FROM views `view`\\n  LEFT JOIN projects project\\n    ON `view`.project_id = project.project_id\\n  LEFT JOIN backend_events backend_event\\n    ON `view`.view_id = backend_event.view_id\\n  LEFT JOIN organizations organization\\n    ON project.organization_id = organization.organization_id\\n  LEFT JOIN users `user`\\n    ON user.organization_id = organization.organization_id\\n ORDER BY 1 ASC, 2 ASC, 3 ASC;\\n\"}','examples/generate_old_workunits',1),(45,'query','{\"view_type\": \"query\", \"query_text\": \"/* Base query is `analytics.user_view_facts`:\\nSELECT organization.name as Organization,\\n       CONCAT(\\\"[\\\", project.name, \\\"]\\\") as Project,\\n       `view`.path as Path,\\n       CAST(AVG(LENGTH(`view`.spec->>\\\"$.query_text\\\")) AS SIGNED) AS `Query length`,\\n       COUNT(DISTINCT backend_event.backend_event_id) AS Events,\\n       COUNT(DISTINCT `user`.user_id) AS `Possible users`\\n  FROM views `view`\\n  LEFT JOIN projects project\\n    ON `view`.project_id = project.project_id\\n  LEFT JOIN backend_events backend_event\\n    ON `view`.view_id = backend_event.view_id\\n  LEFT JOIN organizations organization\\n    ON project.organization_id = organization.organization_id\\n  LEFT JOIN users `user`\\n    ON user.organization_id = organization.organization_id\\n GROUP BY 1, 2, 3\\n ORDER BY 1, 2, 3;\\n \\n \\n  */\\n/* Operations:\\n * - Delete non-workunit columns\\n * - Aggregate workunit columns as necessary\\n * - Add DISTINCT, remove GROUP BY clause\\n * - Add ORDER BY ASC, remove old ORDER BY clause\\n */\\nSELECT DISTINCT organization.name as Organization,\\n       CONCAT(\\\"[\\\", project.name, \\\"]\\\") as Project,\\n       `view`.path as Path,\\n  FROM views `view`\\n  LEFT JOIN projects project\\n    ON `view`.project_id = project.project_id\\n  LEFT JOIN backend_events backend_event\\n    ON `view`.view_id = backend_event.view_id\\n  LEFT JOIN organizations organization\\n    ON project.organization_id = organization.organization_id\\n  LEFT JOIN users `user`\\n    ON user.organization_id = organization.organization_id\\n ORDER BY 1 ASC, 2 ASC, 3 ASC;\"}','examples/generate_new_workunits',1),(51,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT backend_event_id AS event_id,\\n       CONCAT(organization.name, \\\":\\\", backend.name, IFNULL(CONCAT(\\\":[\\\", project.name, \\\"]/\\\", IFNULL(view.path, \\\"\\\")), \\\"\\\")) AS path,\\n       CONCAT(materialization.materialization_type, \\\" materialized \\\", view.view_type) AS method,\\n       materialization.state,\\n       materialization.config,\\n       materialization.context,\\n       backend_event.title,\\n       SUBSTRING_INDEX(backend_event.description, \\\"\\\\n\\\", 1) AS description,\\n       backend_event.created_time AS updated_ts\\n  FROM jasmine_web.backend_events backend_event\\n  LEFT JOIN materializations materialization\\n    ON materialization.materialization_id = backend_event.materialization_id\\n  LEFT JOIN views view\\n    ON view.view_id = backend_event.view_id\\n  LEFT JOIN projects project\\n    ON project.project_id = backend_event.project_id\\n  LEFT JOIN backends backend\\n    ON backend.backend_id = backend_event.backend_id\\n  LEFT JOIN organizations organization\\n    ON organization.organization_id = backend.organization_id\\n ORDER BY event_id DESC;\"}','incremental_demo',1),(52,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT *\\n  FROM jasmine_web.incremental_demo_upsert\\n ORDER BY event_id DESC\\n LIMIT 100;\"}','incremental_demo_from_upsert',1);
/*!40000 ALTER TABLE `views` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Current Database: `jasmine_web`
--

USE `jasmine_web`;

--
-- Final view structure for view `analytics/user_project_facts_from_view_view`
--

/*!50001 DROP VIEW IF EXISTS `analytics/user_project_facts_from_view_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`jasmine_web_su`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `analytics/user_project_facts_from_view_view` AS select `analytics/user_project_facts_view`.`user` AS `user`,`analytics/user_project_facts_view`.`org` AS `org`,`analytics/user_project_facts_view`.`teams` AS `teams`,`analytics/user_project_facts_view`.`project` AS `project`,`analytics/user_project_facts_view`.`view_count` AS `view_count`,`analytics/user_project_facts_view`.`total_query_size` AS `total_query_size` from `analytics/user_project_facts_view` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `analytics/user_project_facts_view`
--

/*!50001 DROP VIEW IF EXISTS `analytics/user_project_facts_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`jasmine_web_su`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `analytics/user_project_facts_view` AS select `user_teams`.`user` AS `user`,`user_teams`.`org` AS `org`,`user_teams`.`teams` AS `teams`,`project`.`name` AS `project`,count(distinct `view`.`view_id`) AS `view_count`,sum(length(json_unquote(json_extract(`view`.`spec`,'$.query_text')))) AS `total_query_size` from (((select `user`.`name` AS `user`,`organization`.`name` AS `org`,group_concat(`team`.`name` separator ',') AS `teams`,`organization`.`organization_id` AS `org_id` from (((`users` `user` left join `team_memberships` `team_membership` on((`user`.`user_id` = `team_membership`.`user_id`))) left join `teams` `team` on((`team_membership`.`team_id` = `team`.`team_id`))) left join `organizations` `organization` on((`user`.`organization_id` = `organization`.`organization_id`))) where (`user`.`user_id` = 1) group by `user`.`name`,`organization`.`name`) `user_teams` left join `projects` `project` on((`project`.`organization_id` = `user_teams`.`org_id`))) left join `views` `view` on((`view`.`project_id` = `project`.`project_id`))) group by `user_teams`.`user`,`user_teams`.`org`,`user_teams`.`teams`,`project`.`name` order by `user_teams`.`user`,`user_teams`.`org`,`user_teams`.`teams`,`project`.`name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `analytics/user_view_facts_view`
--

/*!50001 DROP VIEW IF EXISTS `analytics/user_view_facts_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`jasmine_web_su`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `analytics/user_view_facts_view` AS select `organization`.`name` AS `Organization`,concat('[',`project`.`name`,']') AS `Project`,`view`.`path` AS `Path`,cast(avg(length(json_unquote(json_extract(`view`.`spec`,'$.query_text')))) as signed) AS `Query length`,count(distinct `backend_event`.`backend_event_id`) AS `Events`,count(distinct `user`.`user_id`) AS `Possible users` from ((((`views` `view` left join `projects` `project` on((`view`.`project_id` = `project`.`project_id`))) left join `backend_events` `backend_event` on((`view`.`view_id` = `backend_event`.`view_id`))) left join `organizations` `organization` on((`project`.`organization_id` = `organization`.`organization_id`))) left join `users` `user` on((`user`.`organization_id` = `organization`.`organization_id`))) group by `organization`.`name`,concat('[',`project`.`name`,']'),`view`.`path` order by `organization`.`name`,concat('[',`project`.`name`,']'),`view`.`path` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `incremental_demo_from_upsert_view`
--

/*!50001 DROP VIEW IF EXISTS `incremental_demo_from_upsert_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`jasmine_web_su`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `incremental_demo_from_upsert_view` AS select `incremental_demo_upsert`.`jsmn_auto_id` AS `jsmn_auto_id`,`incremental_demo_upsert`.`event_id` AS `event_id`,`incremental_demo_upsert`.`path` AS `path`,`incremental_demo_upsert`.`method` AS `method`,`incremental_demo_upsert`.`state` AS `state`,`incremental_demo_upsert`.`config` AS `config`,`incremental_demo_upsert`.`context` AS `context`,`incremental_demo_upsert`.`title` AS `title`,`incremental_demo_upsert`.`description` AS `description`,`incremental_demo_upsert`.`updated_ts` AS `updated_ts` from `incremental_demo_upsert` order by `incremental_demo_upsert`.`event_id` desc limit 100 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `incremental_demo_view`
--

/*!50001 DROP VIEW IF EXISTS `incremental_demo_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`jasmine_web_su`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `incremental_demo_view` AS select `backend_event`.`backend_event_id` AS `event_id`,concat(`organization`.`name`,':',`backend`.`name`,ifnull(concat(':[',`project`.`name`,']/',ifnull(`view`.`path`,'')),'')) AS `path`,concat(`materialization`.`materialization_type`,' materialized ',`view`.`view_type`) AS `method`,`materialization`.`state` AS `state`,`materialization`.`config` AS `config`,`materialization`.`context` AS `context`,`backend_event`.`title` AS `title`,substring_index(`backend_event`.`description`,'\n',1) AS `description`,`backend_event`.`created_time` AS `updated_ts` from (((((`backend_events` `backend_event` left join `materializations` `materialization` on((`materialization`.`materialization_id` = `backend_event`.`materialization_id`))) left join `views` `view` on((`view`.`view_id` = `backend_event`.`view_id`))) left join `projects` `project` on((`project`.`project_id` = `backend_event`.`project_id`))) left join `backends` `backend` on((`backend`.`backend_id` = `backend_event`.`backend_id`))) left join `organizations` `organization` on((`organization`.`organization_id` = `backend`.`organization_id`))) order by `backend_event`.`backend_event_id` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!50112 SET @disable_bulk_load = IF (@is_rocksdb_supported, 'SET SESSION rocksdb_bulk_load = @old_rocksdb_bulk_load', 'SET @dummy_rocksdb_bulk_load = 0') */;
/*!50112 PREPARE s FROM @disable_bulk_load */;
/*!50112 EXECUTE s */;
/*!50112 DEALLOCATE PREPARE s */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-09 19:20:01
