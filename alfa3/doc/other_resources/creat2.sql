create database alfaKadrmas;
use alfaKadrmas;
SET autocommit=0;
-- -----------------------------------------------------
-- Table `Brand`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Brand` (
  `idBrand` INT NOT NULL AUTO_INCREMENT,
  `nameBrand` VARCHAR(100) NOT NULL unique,
  `residence` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idBrand`));



-- -----------------------------------------------------
-- Table `Product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Product` (
  `idProduct` INT NOT NULL AUTO_INCREMENT,
  `nameProduct` VARCHAR(100) NOT NULL,
  `weightKG` FLOAT NOT NULL,
  `price` FLOAT NOT NULL,
  `Brand_idBrand` INT NOT NULL,
  PRIMARY KEY (`idProduct`),
  CONSTRAINT `fk_Product_Brand`
    FOREIGN KEY (`Brand_idBrand`)
    REFERENCES `Brand` (`idBrand`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);



-- -----------------------------------------------------
-- Table `User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `userType` ENUM('customer', 'employee') NOT NULL,
  `nickName` VARCHAR(50) NOT NULL unique,
  `cash` FLOAT NULL default 0,
  PRIMARY KEY (`idUser`));



-- -----------------------------------------------------
-- Table `Order`
-- -----------------------------------------------------
insert into `Order`(User_idUser) values(1);
select * from `Order`;
CREATE TABLE IF NOT EXISTS `Order` (
  `idOrder` INT NOT NULL AUTO_INCREMENT,
  `createDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `User_idUser` INT NOT NULL,
  `paid` TINYINT(1) NOT NULL DEFAULT 0,
  `send` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`idOrder`),
  CONSTRAINT `fk_Order_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table `ProductOrder`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ProductOrder` (
  `idProductOrder` INT NOT NULL AUTO_INCREMENT,
  `Order_idOrder` INT NOT NULL,
  `Product_idProduct` INT NOT NULL,
  `amount` INT NOT NULL,
  PRIMARY KEY (`idProductOrder`, `Order_idOrder`, `Product_idProduct`),
  CONSTRAINT `fk_ProductOrder_Order1`
    FOREIGN KEY (`Order_idOrder`)
    REFERENCES `Order` (`idOrder`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_ProductOrder_Product1`
    FOREIGN KEY (`Product_idProduct`)
    REFERENCES `Product` (`idProduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

create user 'public_user'@'localhost' identified by 'password';
grant insert,select,delete,update on alfakadrmas.order to 'public_user'@'localhost';
grant insert,select,delete,update on alfakadrmas.productorder to 'public_user'@'localhost';
grant select on alfakadrmas.product to 'public_user'@'localhost';
grant select on alfakadrmas.brand to 'public_user'@'localhost';
grant update,select on alfakadrmas.user to 'public_user'@'localhost';

grant select on view_product_brand to 'public_user'@'localhost';
grant select on view_order_products to 'public_user'@'localhost';
grant select on view_final_price to 'public_user'@'localhost';


create user 'admin'@'localhost' identified by 'password';
GRANT ALL PRIVILEGES ON alfakadrmas.* TO 'admin'@'localhost';
insert user(userType,nickName) values(2,'admin');

create or replace view view_product_brand as 
select product.idProduct, product.nameProduct, product.weightKG, product.price, brand.nameBrand, brand.residence
from product inner join brand on product.Brand_idBrand = brand.idBrand order by brand.nameBrand,product.nameProduct;
create or replace view view_order_products as 
select `Order`.idOrder,`Order`.createDate,`Order`.paid,`Order`.send,
view_product_brand.nameProduct,view_product_brand.nameBrand,view_product_brand.price,productorder.amount,`Order`.User_idUser
from `Order` inner join productorder on `Order`.idOrder = productorder.Order_idOrder
inner join view_product_brand on productorder.Product_idProduct = view_product_brand.idProduct order by productorder.Order_idOrder;
create or replace view view_final_price as
select sum(view_product_brand.price*productorder.amount),`Order`.User_idUser, `Order`.idOrder
from `Order` inner join productorder on `Order`.idOrder = productorder.Order_idOrder
inner join view_product_brand on productorder.Product_idProduct = view_product_brand.idProduct
group by `Order`.User_idUser,`Order`.idOrder ;
select * from view_final_price where User_idUser = 2;
