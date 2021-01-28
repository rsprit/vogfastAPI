-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: taurus    Database: VOGDB
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `AA_seq`
--

DROP TABLE IF EXISTS `AA_seq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AA_seq` (
  `ID` char(30) NOT NULL,
  `AASeq` longtext,
  KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NT_seq`
--

DROP TABLE IF EXISTS `NT_seq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NT_seq` (
  `ID` char(30) NOT NULL,
  `NTSeq` longtext,
  KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Protein_profile`
--

DROP TABLE IF EXISTS `Protein_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Protein_profile` (
  `ProteinID` char(30) NOT NULL,
  `VOG_ID` char(30) NOT NULL,
  `TaxonID` int NOT NULL,
  KEY `VOG_profile_index_by_protein` (`ProteinID`),
  KEY `TaxonID` (`TaxonID`),
  KEY `VOG_ID` (`VOG_ID`),
  CONSTRAINT `Protein_profile_ibfk_1` FOREIGN KEY (`TaxonID`) REFERENCES `Species_profile` (`TaxonID`),
  CONSTRAINT `Protein_profile_ibfk_2` FOREIGN KEY (`VOG_ID`) REFERENCES `VOG_profile` (`VOG_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Species_profile`
--

DROP TABLE IF EXISTS `Species_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Species_profile` (
  `SpeciesName` char(100) NOT NULL,
  `TaxonID` int NOT NULL,
  `Phage` tinyint(1) NOT NULL,
  `Source` char(100) NOT NULL,
  `Version` int NOT NULL,
  PRIMARY KEY (`TaxonID`),
  CONSTRAINT `Species_profile_chk_1` CHECK ((`Phage` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `VOG_profile`
--

DROP TABLE IF EXISTS `VOG_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VOG_profile` (
  `VOG_ID` char(30) NOT NULL,
  `ProteinCount` int NOT NULL,
  `SpeciesCount` int NOT NULL,
  `FunctionalCategory` char(30) NOT NULL,
  `Proteins` longtext,
  `Consensus_func_description` char(100) NOT NULL,
  `GenomesInGroup` int NOT NULL,
  `GenomesTotal` int NOT NULL,
  `Ancestors` text,
  `StringencyHigh` tinyint(1) NOT NULL,
  `StringencyMedium` tinyint(1) NOT NULL,
  `StringencyLow` tinyint(1) NOT NULL,
  `VirusSpecific` tinyint(1) NOT NULL,
  `NumPhages` int NOT NULL,
  `NumNonPhages` int NOT NULL,
  `PhageNonphage` text,
  PRIMARY KEY (`VOG_ID`),
  UNIQUE KEY `VOG_profile_index` (`VOG_ID`,`FunctionalCategory`),
  KEY `ix_VOG_profile_VOG_ID` (`VOG_ID`),
  CONSTRAINT `VOG_profile_chk_1` CHECK ((`StringencyHigh` in (0,1))),
  CONSTRAINT `VOG_profile_chk_2` CHECK ((`StringencyMedium` in (0,1))),
  CONSTRAINT `VOG_profile_chk_3` CHECK ((`StringencyLow` in (0,1))),
  CONSTRAINT `VOG_profile_chk_4` CHECK ((`VirusSpecific` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-28 14:44:47
