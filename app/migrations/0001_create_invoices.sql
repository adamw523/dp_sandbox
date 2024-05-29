-- 
create extension if not exists "uuid-ossp";
create table customers (
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    email text unique not null,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp
);
create table invoices (
    id uuid primary key default uuid_generate_v4(),
    customer_id uuid not null,
    invoice_date date not null,
    total_amount_cents int not null,
    status varchar(20) not null default 'pending',
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp
);
create table invoice_line_items (
    id uuid primary key default uuid_generate_v4(),
    invoice_id uuid not null,
    product_id uuid not null,
    quantity int not null,
    unit_price_cents numeric not null,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    foreign key (invoice_id) references invoices (id) on delete cascade
);
create index idx_invoice_date on invoices (invoice_date);
create index idx_invoice_customer_id on invoices (customer_id);
create index idx_line_item_invoice_id on invoice_line_items (invoice_id);