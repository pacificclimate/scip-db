These scripts allow mostly-automatic updating of the salmon occurrence database. It is less polished than some of PCIC's other alembic systems, and may require a bit of setup. Improvements are planned.

To use:

* edit the `sqlalchemy.url` connection string in `alembic.ini`, either to substitute in a password or to point to a different database
* optionally edit the `salmon_schema` variable in the migrations in the `versions` folder (the SCIP backend expects a schema named "salmon_geometry"
* run alembic with `alembic upgrade head` to initialize or upgrade the database and schema you specified