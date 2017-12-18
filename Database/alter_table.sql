alter table products
modify pro_time varchar(45);


alter table products
modify pro_name longtext;

alter table products
modify pro_pic longtext;

alter table products
modify pro_color longtext;

alter table products
add RGB varchar(45);


create view product_effect
as select p.pro_id, p.pro_brand, p.pro_class, p.pro_color, p.pro_name, p.pro_pic, p.pro_price, p.pro_score, p.pro_time, e.Coloring, e.Concealer , e.Distinctness, e.Durability, e.Moisture, e.Naturalness, e.Pushing_evenness, e.Refreshing, e.Saturation, e.Sticking, e.Transparency, e.Waterproof
	from products p, effect e
	where p.pro_id = e.pro_id ;