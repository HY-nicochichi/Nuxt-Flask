\set user `echo "${POSTGRES_USER}"`
\set db_test `echo "${POSTGRES_DB}_test"`

CREATE DATABASE :"db_test" OWNER :"user";
