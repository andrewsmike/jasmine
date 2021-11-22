-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: jasmine_web
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
INSERT INTO `alembic_version` VALUES ('8817963694c9');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

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
  CONSTRAINT `backend_event_backend` FOREIGN KEY (`backend_id`) REFERENCES `backends` (`backend_id`),
  CONSTRAINT `backend_event_view` FOREIGN KEY (`view_id`) REFERENCES `views` (`view_id`),
  CONSTRAINT `project_event_view` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backend_events`
--

LOCK TABLES `backend_events` WRITE;
/*!40000 ALTER TABLE `backend_events` DISABLE KEYS */;
INSERT INTO `backend_events` VALUES (1,'Created backend blahblah with view','blahblah','2021-09-29 04:54:52',NULL,1,1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `views`
--

LOCK TABLES `views` WRITE;
/*!40000 ALTER TABLE `views` DISABLE KEYS */;
INSERT INTO `views` VALUES (1,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT user_teams.`user`,\\n       user_teams.org,\\n       user_teams.teams,\\n       project.name as project,\\n       COUNT(DISTINCT `view`.view_id) AS view_count,\\n       SUM(LENGTH(`view`.spec->>\\\"$.query_text\\\")) AS total_query_size\\n  FROM (\\nSELECT `user`.name as `user`, organization.name as org, GROUP_CONCAT(team.name) as teams, organization.organization_id as org_id \\n  FROM users `user`\\n  LEFT JOIN team_memberships team_membership\\n    ON `user`.user_id = team_membership.user_id\\n  LEFT JOIN teams team\\n    ON team_membership.team_id = team.team_id\\n  LEFT JOIN organizations organization\\n    ON `user`.organization_id = organization.organization_id\\n WHERE `user`.user_id = 1\\n GROUP BY 1, 2\\n     ) user_teams\\n  LEFT JOIN projects project\\n    ON project.organization_id = user_teams.org_id\\n  LEFT JOIN views `view`\\n    ON `view`.project_id = project.project_id\\n GROUP BY 1, 2, 3, 4\\n ORDER BY 1, 2, 3, 4;\"}','analytics/user_project_facts',1),(2,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT * /* BLAHHHH*/\\n  FROM my_table a /* BLAH  ueathnu*/    LEFT JOIN my_other_table b\\n    ON a.other_table_id = b.id\\n GROUP BY 1, 2\\n LIMIT 1;\"}','trivial/nonsense',1),(28,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT organization.name as Organization,\\n       CONCAT(\\\"[\\\", project.name, \\\"]\\\") as Project,\\n       `view`.path as Path,\\n       CAST(AVG(LENGTH(`view`.spec->>\\\"$.query_text\\\")) AS SIGNED) AS `Query length`,\\n       COUNT(DISTINCT backend_event.backend_event_id) AS Events,\\n       COUNT(DISTINCT `user`.user_id) AS `Possible users`\\n  FROM views `view`\\n  LEFT JOIN projects project\\n    ON `view`.project_id = project.project_id\\n  LEFT JOIN backend_events backend_event\\n    ON `view`.view_id = backend_event.view_id\\n  LEFT JOIN organizations organization\\n    ON project.organization_id = organization.organization_id\\n  LEFT JOIN users `user`\\n    ON user.organization_id = organization.organization_id\\n GROUP BY 1, 2, 3\\n ORDER BY 1, 2, 3;\\n \"}','analytics/user_view_facts',1),(34,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT 1 AS result\\n  FROM DUAL\\n WHERE 3 > 2\\n LIMIT 1;\"}','trivial/dual',1),(39,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT 1 LIMIT 1;\"}','trivial/limit 1',1),(40,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT *\\n  FROM jasmine_web.views\\n LIMIT 10;\"}','raw/views',1),(41,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT 1\"}','scratch/bad_power_0cf3',1),(42,'query','{\"view_type\": \"query\", \"query_text\": \"SELECT *\\n  FROM users `user`\\n  LEFT JOIN team_memberships team_membership\\n  LEFT JOIN teams team\\n    ON team_membership.team_id = team.team_id\\n    ON `user`.user_id = team_membership.user_id;\\n\"}','trivial/horror_show',1);
/*!40000 ALTER TABLE `views` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-08 21:10:39
