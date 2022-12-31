create table if not exists image (
  id int not null primary key,
  doc_id text not null,
  photographer text,
  caption text not null,
  description text not null default '',
  location text,
  date date,
  url_path text not null
)