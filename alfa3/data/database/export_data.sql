-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: alfakadrmas
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brand` (
  `idBrand` int NOT NULL AUTO_INCREMENT,
  `nameBrand` varchar(100) NOT NULL,
  `residence` varchar(100) NOT NULL,
  PRIMARY KEY (`idBrand`),
  UNIQUE KEY `nameBrand` (`nameBrand`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brand`
--

LOCK TABLES `brand` WRITE;
/*!40000 ALTER TABLE `brand` DISABLE KEYS */;
INSERT INTO `brand` VALUES (1,'Nike','New York'),(2,'Prusa','Prague'),(3,'CheckPoint','Isreal'),(4,'Samsung','China'),(5,'Apple','New York');
/*!40000 ALTER TABLE `brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `idOrder` int NOT NULL AUTO_INCREMENT,
  `createDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `User_idUser` int NOT NULL,
  `paid` tinyint(1) NOT NULL DEFAULT '0',
  `send` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idOrder`),
  KEY `fk_Order_User1` (`User_idUser`),
  CONSTRAINT `fk_Order_User1` FOREIGN KEY (`User_idUser`) REFERENCES `user` (`idUser`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,'2023-02-03 19:07:37',2,1,1),(2,'2023-02-03 19:07:37',2,1,0),(3,'2023-02-03 19:07:37',2,0,0);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `idProduct` int NOT NULL AUTO_INCREMENT,
  `nameProduct` varchar(100) NOT NULL,
  `weightKG` float NOT NULL,
  `price` float NOT NULL,
  `Brand_idBrand` int NOT NULL,
  PRIMARY KEY (`idProduct`),
  KEY `fk_Product_Brand` (`Brand_idBrand`),
  CONSTRAINT `fk_Product_Brand` FOREIGN KEY (`Brand_idBrand`) REFERENCES `brand` (`idBrand`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Running shoes',0.03,59.99,2),(2,'3d printer',0.4,500,1),(3,'prusa t-shirt',0.02,20.49,1),(4,'Samsung phone',0.1,249.99,3),(5,'Magic mouse',0.01,550,4);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productorder`
--

DROP TABLE IF EXISTS `productorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productorder` (
  `idProductOrder` int NOT NULL AUTO_INCREMENT,
  `Order_idOrder` int NOT NULL,
  `Product_idProduct` int NOT NULL,
  `amount` int NOT NULL,
  PRIMARY KEY (`idProductOrder`,`Order_idOrder`,`Product_idProduct`),
  KEY `fk_ProductOrder_Order1` (`Order_idOrder`),
  KEY `fk_ProductOrder_Product1` (`Product_idProduct`),
  CONSTRAINT `fk_ProductOrder_Order1` FOREIGN KEY (`Order_idOrder`) REFERENCES `order` (`idOrder`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_ProductOrder_Product1` FOREIGN KEY (`Product_idProduct`) REFERENCES `product` (`idProduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productorder`
--

LOCK TABLES `productorder` WRITE;
/*!40000 ALTER TABLE `productorder` DISABLE KEYS */;
INSERT INTO `productorder` VALUES (1,1,2,2),(2,1,4,1),(3,2,3,1),(4,2,1,3),(5,3,5,1),(6,3,3,2);
/*!40000 ALTER TABLE `productorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `idUser` int NOT NULL AUTO_INCREMENT,
  `userType` enum('customer','employee') NOT NULL,
  `nickName` varchar(50) NOT NULL,
  `cash` float DEFAULT '0',
  PRIMARY KEY (`idUser`),
  UNIQUE KEY `nickName` (`nickName`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'employee','admin',100),(2,'customer','pepa',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `view_final_price`
--

DROP TABLE IF EXISTS `view_final_price`;
/*!50001 DROP VIEW IF EXISTS `view_final_price`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_final_price` AS SELECT 
 1 AS `sum(view_product_brand.price*productorder.amount)`,
 1 AS `User_idUser`,
 1 AS `idOrder`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_order_products`
--

DROP TABLE IF EXISTS `view_order_products`;
/*!50001 DROP VIEW IF EXISTS `view_order_products`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_order_products` AS SELECT 
 1 AS `idOrder`,
 1 AS `createDate`,
 1 AS `paid`,
 1 AS `send`,
 1 AS `nameProduct`,
 1 AS `nameBrand`,
 1 AS `price`,
 1 AS `amount`,
 1 AS `User_idUser`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_product_brand`
--

DROP TABLE IF EXISTS `view_product_brand`;
/*!50001 DROP VIEW IF EXISTS `view_product_brand`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_product_brand` AS SELECT 
 1 AS `idProduct`,
 1 AS `nameProduct`,
 1 AS `weightKG`,
 1 AS `price`,
 1 AS `nameBrand`,
 1 AS `residence`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `view_final_price`
--

/*!50001 DROP VIEW IF EXISTS `view_final_price`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_final_price` AS select sum((`view_product_brand`.`price` * `productorder`.`amount`)) AS `sum(view_product_brand.price*productorder.amount)`,`order`.`User_idUser` AS `User_idUser`,`order`.`idOrder` AS `idOrder` from ((`order` join `productorder` on((`order`.`idOrder` = `productorder`.`Order_idOrder`))) join `view_product_brand` on((`productorder`.`Product_idProduct` = `view_product_brand`.`idProduct`))) group by `order`.`User_idUser`,`order`.`idOrder` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_order_products`
--

/*!50001 DROP VIEW IF EXISTS `view_order_products`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_order_products` AS select `order`.`idOrder` AS `idOrder`,`order`.`createDate` AS `createDate`,`order`.`paid` AS `paid`,`order`.`send` AS `send`,`view_product_brand`.`nameProduct` AS `nameProduct`,`view_product_brand`.`nameBrand` AS `nameBrand`,`view_product_brand`.`price` AS `price`,`productorder`.`amount` AS `amount`,`order`.`User_idUser` AS `User_idUser` from ((`order` join `productorder` on((`order`.`idOrder` = `productorder`.`Order_idOrder`))) join `view_product_brand` on((`productorder`.`Product_idProduct` = `view_product_brand`.`idProduct`))) order by `productorder`.`Order_idOrder` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_product_brand`
--

/*!50001 DROP VIEW IF EXISTS `view_product_brand`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_product_brand` AS select `product`.`idProduct` AS `idProduct`,`product`.`nameProduct` AS `nameProduct`,`product`.`weightKG` AS `weightKG`,`product`.`price` AS `price`,`brand`.`nameBrand` AS `nameBrand`,`brand`.`residence` AS `residence` from (`product` join `brand` on((`product`.`Brand_idBrand` = `brand`.`idBrand`))) order by `brand`.`nameBrand`,`product`.`nameProduct` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

--
-- Users and privilages
--
drop user IF exists 'public_user'@'localhost';
create user 'public_user'@'localhost' identified by 'password';
grant insert,select,delete,update on alfakadrmas.order to 'public_user'@'localhost';
grant insert,select,delete,update on alfakadrmas.productorder to 'public_user'@'localhost';
grant select on alfakadrmas.product to 'public_user'@'localhost';
grant select on alfakadrmas.brand to 'public_user'@'localhost';
grant update,select on alfakadrmas.user to 'public_user'@'localhost';

grant select on view_product_brand to 'public_user'@'localhost';
grant select on view_order_products to 'public_user'@'localhost';
grant select on view_final_price to 'public_user'@'localhost';

drop user if exists  'admin'@'localhost';
create user 'admin'@'localhost' identified by 'password';
GRANT ALL PRIVILEGES ON alfakadrmas.* TO 'admin'@'localhost';


-- Dump completed on 2023-02-03 19:17:26
-- Alfa 3
-- name:Antonín Kadrmas
-- mail:kadrmas@spsejecna.cz
-- date:1.30.2023
-- school:Secondary Technical School of Electrical Engineering Jecna 30, Prague, Czech Republic
-- school project

