-- CREATE DATABASE url_production;


DROP TABLE IF EXISTS clicks_analytics CASCADE;
DROP TABLE IF EXISTS urls CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    pass_hash CHAR(60) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE urls(
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NULL DEFAULT NULL,
    long_url VARCHAR(2048) NOT NULL,
    short_key VARCHAR(10) UNIQUE NOT NULL,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE 
);

CREATE TABLE clicks_analytics(
    id BIGSERIAL PRIMARY KEY,
    url_id BIGINT REFERENCES urls(id) ON DELETE CASCADE,
    clicked_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_agent VARCHAR(511) NOT NULL,
    country_code CHAR(2) NOT NULL,
    referrer VARCHAR(2048)
);


CREATE INDEX idx_urls_expiration 
ON urls (expires_at) 
WHERE expires_at IS NOT NULL;

CREATE INDEX idx_analytics_url_date 
ON clicks_analytics (url_id, clicked_at DESC);