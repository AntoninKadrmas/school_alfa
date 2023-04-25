insert into brand(nameBrand,residence) values ('Nike','New York');
insert into brand(nameBrand,residence) values ('Prusa','Prague');
insert into brand(nameBrand,residence) values ('CheckPoint','Isreal');
insert into brand(nameBrand,residence) values ('Samsung','China');
insert into brand(nameBrand,residence) values ('Apple','New York');


insert into user(userType,nickName,cash) values(2,'admin',100);
insert into user(userType,nickName,cash) values(1,'pepa',0);


insert into product(nameProduct,weightKG,price,Brand_idBrand) values ('Running shoes',0.03,59.99,0);
insert into product(nameProduct,weightKG,price,Brand_idBrand) values ('3d printer',0.4, 500, 1);
insert into product(nameProduct,weightKG,price,Brand_idBrand) values ('prusa t-shirt',0.02,20.49,1);
insert into product(nameProduct,weightKG,price,Brand_idBrand) values ('Samsung phone',0.1, 249.99,3);
insert into product(nameProduct,weightKG,price,Brand_idBrand) values ('Magic mouse',0.01,550,4);

insert into `order`(User_idUser) values(2); 
insert into `order`(User_idUser) values(2); 
insert into `order`(User_idUser) values(2); 
update `order` set paid=1, send =1 where `order`.idOrder = 1;
update `order` set paid=1 where `order`.idOrder = 2;

insert into orderproduct(Order_idOrder,Product_idProduct,amount) values(1,2,2);
insert into orderproduct(Order_idOrder,Product_idProduct,amount) values(1,4,1);
insert into orderproduct(Order_idOrder,Product_idProduct,amount) values(2,3,1);
insert into orderproduct(Order_idOrder,Product_idProduct,amount) values(2,1,3);
insert into orderproduct(Order_idOrder,Product_idProduct,amount) values(3,5,1);
insert into orderproduct(Order_idOrder,Product_idProduct,amount) values(3,3,2);




