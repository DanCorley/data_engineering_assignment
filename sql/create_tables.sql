create table if not exists olist_customers_dataset (
  customer_id varchar(255) not null,
  customer_unique_id varchar(255) not null,
  customer_zip_code_prefix integer,
  customer_city text,
  customer_state text,
  primary key (customer_id)
);

create table if not exists olist_orders_dataset (
  order_id varchar(255) not null,
  customer_id varchar(255),
  order_status text,
  order_purchase_timestamp timestamp,
  order_approved_at timestamp,
  order_delivered_carrier_date timestamp,
  order_delivered_customer_date timestamp,
  order_estimated_delivery_date timestamp,
  primary key (order_id),
  constraint fk_customer
    foreign key(customer_id)
      references olist_customers_dataset(customer_id)
);

create table if not exists olist_products_dataset (
  product_id varchar(255) not null,
  product_category_name text,
  product_name_lenght integer,
  product_description_lenght integer,
  product_photos_qty integer,
  product_weight_g integer,
  product_length_cm integer,
  product_height_cm integer,
  product_width_cm integer,
  primary key (product_id)
);

create table if not exists olist_order_items_dataset (
  order_id varchar(255) not null,
  order_item_id smallint,
  product_id text,
  seller_id text,
  shipping_limit_date timestamp,
  price decimal,
  freight_value decimal,
  constraint fk_order
    foreign key(order_id)
      references olist_orders_dataset(order_id),
  constraint fk_product
    foreign key(product_id)
      references olist_products_dataset(product_id)
);

-- clear up old data if you've already run script
truncate table olist_customers_dataset cascade;
truncate table olist_orders_dataset cascade;
truncate table olist_products_dataset cascade;
truncate table olist_order_items_dataset;
