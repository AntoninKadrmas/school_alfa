-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema AlfaKadrmas
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `Brand`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Brand` (
  `idBrand` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `residence` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idBrand`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Product` (
  `idProduct` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `weightKG` FLOAT NOT NULL,
  `price` FLOAT NOT NULL,
  `Brand_idBrand` INT NOT NULL,
  PRIMARY KEY (`idProduct`),
  INDEX `fk_Product_Brand_idx` (`Brand_idBrand` ASC) VISIBLE,
  CONSTRAINT `fk_Product_Brand`
    FOREIGN KEY (`Brand_idBrand`)
    REFERENCES `Brand` (`idBrand`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `type` ENUM('Customer', 'Employee') NOT NULL,
  `nickName` VARCHAR(50) NOT NULL,
  `cash` FLOAT NULL,
  PRIMARY KEY (`idUser`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Order` (
  `idOrder` INT NOT NULL AUTO_INCREMENT,
  `createDate` DATETIME NOT NULL,
  `User_idUser` INT NOT NULL,
  `paid` TINYINT(1) NOT NULL DEFAULT 0,
  `send` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`idOrder`),
  INDEX `fk_Order_User1_idx` (`User_idUser` ASC) VISIBLE,
  CONSTRAINT `fk_Order_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ProductOrder`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ProductOrder` (
  `idProductOrder` INT NOT NULL AUTO_INCREMENT,
  `Order_idOrder` INT NOT NULL,
  `Product_idProduct` INT NOT NULL,
  `amount` INT NOT NULL,
  PRIMARY KEY (`idProductOrder`, `Order_idOrder`, `Product_idProduct`),
  INDEX `fk_ProductOrder_Order1_idx` (`Order_idOrder` ASC) VISIBLE,
  INDEX `fk_ProductOrder_Product1_idx` (`Product_idProduct` ASC) VISIBLE,
  CONSTRAINT `fk_ProductOrder_Order1`
    FOREIGN KEY (`Order_idOrder`)
    REFERENCES `Order` (`idOrder`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_ProductOrder_Product1`
    FOREIGN KEY (`Product_idProduct`)
    REFERENCES `Product` (`idProduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
