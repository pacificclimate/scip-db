# salmon-occurrence
ORM for a database of BC salmon population. 

There are two main sections of the database. 

The `region` table describes regions a user might be interested in, such as watersheds, or drainage basins. Each region has a `kind` (currently ony `watershed` or `basin` but probably more someday), an outlet, a name, a code, and a geometric boundary. There are intended to be offered to users by menus in the front end.

The `population` table describes populations of salmon - species, location, life cycle, and data sources are in linked tables. 

The overall purpose of this database is to allow a user to select a predefined region, or even supply their own region, and view information about the salmon populations in that area.
