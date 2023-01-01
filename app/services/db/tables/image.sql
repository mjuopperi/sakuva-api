create table if not exists image (
  id int not null primary key,
  photographer text,
  caption text not null,
  description text not null default '',
  location text,
  date date,
  url_path text not null
)
