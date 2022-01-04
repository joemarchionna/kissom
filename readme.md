kissom - keep it simple stupid object mapper
============================================
Kissom provides a object store manager that uses a configuration file to map database fields to object (dictionary) fields, as
opposed to creating a class with the fields and mapping the fields in code. The manager allows different database adapters to 
be inserted into the manager to allow access to that type of database. The original design was implemented for use with 
postgresql. The configuration file can be written automatically if the database supports querying of the table structure. 

Installation
============
<p>This is meant to be used as a library. To install this project in another project run the following command:

```
    $ pip install git+ssh://git@github.com/joemarchionna/kissom.git
```
My plan is to put this up on PyPI, but until that happens, this how to add it

Dependancies
============
<p>This project doesn't have any dependancies but does require you to use an adapter for the specific data store 
you plan on using. As of this release, only an adapter for PostgreSQL exists:

* kissom_pg

The plan is to add additional adapters.

Use
===
Using the kissom_pg package to access a PostgreSQL database. Let's say you create the following table via psql:

```
create schema example;
create sequence example.car_seq start 1001;
create table example.car(
    id int primary key default nextval('example.car_seq'),
    make text not null,
    model text not null,
    color text,
    gross_kg float,
    manufactured timestamp default (now() AT TIME ZONE 'utc')
);
```

Create the manager and insert a record:

```
from kissom.storeManager import StoreManager
from kissom_pg.pgAdapter import PgAdapter

record = {
        "make": "vw",
        "model": "rabbit",
        "color": "white",
        "grossKg": 845,
    }

mgr = StoreManager(adapter=PgAdapter(connectionString="<add your conn str here>"))
insertedRecord = mgr.insert(obj=record, fqtn="example.car")
```
Note that the fqtn can be included in the record with the key "\_\_fqtn__". Also note that the manager 
will convert grossKg to gross_kg.

Getting all of the stored records in the table:

```
records = mgr.select(fqtn = "example.car")
```
or a specific record:

```
records = mgr.select(fqtn="example.car", conditions={"fieldName": "color", "fieldValue": "white"})
```

Update the record changing the color to 'red':

```
mgr.update(obj={"__fqtn__": "example.car", "id": 1001, "color": "red"})
```

Lastly, close the connection:

```
mgr.adapter.closeConnection()
```

Tests
=====
To run all of the tests in this project run the following from the project root folder:

```
python -m unittest discover -s kissom/tests/
```

To run a specific test in this project run the following from the project root folder:

```
python -m unittest kissom/tests/<specific test class>.py
```

Code Formatting
===============
<p>Code formatting was done using BLACK.
<p>To bulk format files, the following command will work:

```
    $ black . -l 119
```

====
