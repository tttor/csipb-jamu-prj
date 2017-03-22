# Database-related source code

## Steps
* aim for connectivity data.
* aim for metadata of each item.

## Commands

### login via psql (9.6.1)
psql ijah  -h 127.0.0.1 -d ijah

### dump
* $ sudo -u ijah pg_dump ijah > ijah.sql
* ijah=> \copy protein to /home/tor/protein.csv csv header
* ijah=> \copy (SELECT com_cas_id FROM compound) TO '/home/tor/tmp/test.csv' With CSV;

### import
psql ijah  -h 127.0.0.1 -d ijah < ijah_201612141709.sql

### apps.cs
* sudo -u postgres psql mydb
* sudo -u postgres createdb mydb
* sudo -u postgres createuser tor
* sudo -u postgres dropdb ijah
* sudo -u postgres psql
* postgres=# \password [role]

## Queries
```sql
* CREATE INDEX com_sim_idx ON compound_similarity (com_id_i,com_id_j,method);
  * CREATE INDEX pro_sim_idx ON protein_similarity (pro_id_i,pro_id_j,method);

* ALTER SEQUENCE [tablename]_[id]_seq RESTART WITH 1
  * ALTER SEQUENCE user_msg_id_seq RESTART WITH 1;

* ALTER TABLE compound DROP COLUMN com_similarity_simcomp;

* ALTER TABLE plant ADD COLUMN pla_idr_name varchar(256);
  * ALTER TABLE protein ADD COLUMN pro_pdb_id text;

* SELECT COUNT(DISTINCT (c.com_id)) from compound as c ,plant_vs_compound as pc
  where c.com_id=pc.com_id;

* CREATE TABLE compound_similarity (
                com_id_i varchar(12) NOT NULL,
                com_id_j varchar(12) NOT NULL,
                method varchar(64) NOT NULL,
                value float(16) NOT NULL,
                time_stamp timestamp DEFAULT now()
                );

* SELECT
  count(distinct plant.pla_id)
  FROM
  plant
  LEFT JOIN
  plant_vs_compound
  ON
  plant.pla_id = plant_vs_compound.pla_id
  WHERE
  plant_vs_compound.pla_id IS NULL;

* DELETE FROM compound where com_id IN (
  SELECT
  distinct compound.com_id
  FROM
  compound
  LEFT JOIN
  plant_vs_compound
  ON
  compound.com_id = plant_vs_compound.com_id
  WHERE
  plant_vs_compound.com_id IS NULL
  );
```
