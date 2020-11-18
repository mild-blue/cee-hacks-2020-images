--
-- file: common/db/migrations/0001.initial-schema.rollback.sql
--

DROP TABLE IF EXISTS job_transitions CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS app_users CASCADE;

DROP TYPE IF EXISTS JOB_STATUS;
DROP TYPE IF EXISTS APP_USER_ROLE;

DROP FUNCTION IF EXISTS set_created_at;
DROP FUNCTION IF EXISTS set_updated_at;
