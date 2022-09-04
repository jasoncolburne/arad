set -euo pipefail

apt-get -y install postgresql-client

echo "create EXTENSION if not EXISTS pgcrypto;" | PGPASSWORD="${POSTGRES_PASSWORD}" psql -U "${POSTGRES_USER}" -h 127.0.0.1

echo "SELECT 'CREATE DATABASE ${DATABASE_NAME}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${DATABASE_NAME}')\gexec" | PGPASSWORD="${POSTGRES_PASSWORD}" psql -U "${POSTGRES_USER}" -h 127.0.0.1
PGPASSWORD="${POSTGRES_PASSWORD}" psql -U "${POSTGRES_USER}" -h 127.0.0.1 << PLPGSQL
DO
\$do\$
BEGIN
  IF NOT EXISTS (
    SELECT FROM pg_catalog.pg_roles
    WHERE  rolname = '${DATABASE_USER}') THEN
    CREATE ROLE ${DATABASE_USER} LOGIN PASSWORD '${DATABASE_PASSWORD}';
  END IF;
END
\$do\$;
PLPGSQL
PGPASSWORD="${POSTGRES_PASSWORD}" psql -U "${POSTGRES_USER}" -h 127.0.0.1 -c "GRANT ALL PRIVILEGES ON DATABASE ${DATABASE_NAME} TO ${DATABASE_USER};"
