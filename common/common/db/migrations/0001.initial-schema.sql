--
-- file: common/db/migrations/0001.initial-schema.sql
--

CREATE TYPE APP_USER_ROLE AS ENUM (
    'ADMIN',
    'SERVICE'
    );

CREATE TYPE JOB_STATUS AS ENUM (
    'INITIAL',
    'QUEUED',
    'IN_PROGRESS',
    'FINISHED',
    'FAILURE'
    );

CREATE TABLE app_users
(
    id         BIGSERIAL     NOT NULL,
    username   TEXT          NOT NULL, -- serves as username
    pass_hash  TEXT          NOT NULL,
    role       APP_USER_ROLE NOT NULL,
    created_at TIMESTAMPTZ   NOT NULL,
    updated_at TIMESTAMPTZ   NOT NULL,
    deleted_at TIMESTAMPTZ,
    CONSTRAINT pk_app_users__id PRIMARY KEY (id),
    CONSTRAINT uk_app_users__email UNIQUE (username)
);

CREATE TABLE jobs
(
    id          UUID        NOT NULL,
    app_user_id BIGSERIAL   NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL,
    deleted_at  TIMESTAMPTZ,
    CONSTRAINT pk_jobs__id PRIMARY KEY (id),
    CONSTRAINT fk_jobs__app_user_id FOREIGN KEY (app_user_id) REFERENCES app_users (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE job_transitions
(
    id         BIGSERIAL   NOT NULL,
    status     JOB_STATUS  NOT NULL,
    job_id     UUID        NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    deleted_at TIMESTAMPTZ,
    CONSTRAINT pk_job_transitions__id PRIMARY KEY (id),
    CONSTRAINT fk_job_transitions__job_id FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uk_job_transitions__status_job_id UNIQUE (status, job_id)
);

-- BEFORE insert function for trigger
CREATE OR REPLACE FUNCTION set_created_at() RETURNS TRIGGER
AS
$BODY$
BEGIN
    new.created_at := now();
    new.updated_at := new.created_at;
    RETURN new;
END;
$BODY$
    LANGUAGE plpgsql;

-- BEFORE update function for trigger
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER
AS
$BODY$
BEGIN
    new.updated_at := now();
    RETURN new;
END;
$BODY$
    LANGUAGE plpgsql;


-- These two scripts must be executed for each newly added table.
DO
$$
    DECLARE
        t TEXT;
    BEGIN
        FOR t IN
            SELECT table_name FROM information_schema.columns WHERE column_name = 'created_at'
            LOOP
                EXECUTE format('CREATE TRIGGER trg_%I_set_created_at
                    BEFORE INSERT ON %I
                    FOR EACH ROW EXECUTE PROCEDURE set_created_at()', t, t);
            END LOOP;
    END;
$$
LANGUAGE plpgsql;

DO
$$
    DECLARE
        t TEXT;
    BEGIN
        FOR t IN
            SELECT table_name FROM information_schema.columns WHERE column_name = 'updated_at'
            LOOP
                EXECUTE format('CREATE TRIGGER trg_%I_set_updated_at
                    BEFORE UPDATE ON %I
                    FOR EACH ROW EXECUTE PROCEDURE set_updated_at()', t, t);
            END LOOP;
    END;
$$
LANGUAGE plpgsql;

INSERT INTO app_users(id, username, pass_hash, role, created_at, updated_at)
VALUES (1, 'admin', 'admin', 'ADMIN', now(), now())
