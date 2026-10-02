CREATE TABLE IF NOT EXISTS roles (
    id              INT             GENERATED ALWAYS AS IDENTITY,
    name            VARCHAR(255)    NOT NULL,

    CONSTRAINT pk_roles PRIMARY KEY (id),
    CONSTRAINT uk_roles_name UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS users (
    id                  INT             GENERATED ALWAYS AS IDENTITY,
    name                VARCHAR(255)    NOT NULL,
    username            VARCHAR(255)    NOT NULL,
    nickname            VARCHAR(255)    NOT NULL,
    email               VARCHAR(255)    NOT NULL,
    role_id             INT             NOT NULL,
    salt                VARCHAR(255)    NOT NULL,
    password_hash       VARCHAR(255)    NOT NULL,
    status              VARCHAR(255)    NOT NULL DEFAULT 'ACTIVE',
    created_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_users PRIMARY KEY (id),
    CONSTRAINT uk_users_username UNIQUE (username),
    CONSTRAINT uk_users_nickname UNIQUE (nickname),
    CONSTRAINT uk_users_email UNIQUE (email),
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles (id)
);

CREATE TABLE IF NOT EXISTS animes (
    id                  INT             GENERATED ALWAYS AS IDENTITY,
    title               VARCHAR(255)    NOT NULL,
    title_english       VARCHAR(255)    NULL,
    cover_url           VARCHAR(255)    NOT NULL,
    is_finished         BOOLEAN         NOT NULL DEFAULT FALSE,
    episode_duration    INT             NULL,

    CONSTRAINT pk_animes PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS episodes (
    id                  INT             GENERATED ALWAYS AS IDENTITY,
    name                VARCHAR(255)    NOT NULL,
    description         VARCHAR(255)    NULL,
    number              INT             NOT NULL,
    air_date            DATE            NULL,
    anime_id            INT             NOT NULL,

    CONSTRAINT pk_episodes PRIMARY KEY (id),
    CONSTRAINT uk_episodes_anime_number UNIQUE (anime_id, number),
    CONSTRAINT fk_episodes_anime FOREIGN KEY (anime_id) REFERENCES animes (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS watched_episode (
    id                  INT             GENERATED ALWAYS AS IDENTITY,
    user_id             INT             NOT NULL,
    episode_id          INT             NOT NULL,
    status              VARCHAR(255)    NOT NULL,
    score               SMALLINT        NULL,
    watched_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_watched_episode PRIMARY KEY (id),
    CONSTRAINT uk_watched_episode_user_episode UNIQUE (user_id, episode_id),
    CONSTRAINT fk_watched_episode_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_watched_episode_episode FOREIGN KEY (episode_id) REFERENCES episodes (id) ON DELETE CASCADE,
    CONSTRAINT ck_watched_episode_score CHECK (score IS NULL OR score BETWEEN 1 AND 10)
);

CREATE INDEX IF NOT EXISTS ix_users_role_id ON users (role_id);
CREATE INDEX IF NOT EXISTS ix_watched_episode_episode_id ON watched_episode (episode_id);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();
