CREATE TABLE IF NOT EXISTS visits(
    visit_id VARCHAR(255),
    source VARCHAR(255),
    user_agent VARCHAR(255),
    datetime TIMESTAMP
);

CREATE TABLE IF NOT EXISTS registrations(
    datetime TIMESTAMP,
    user_id VARCHAR(255),
    email VARCHAR(255),
    source VARCHAR(255),
    registration_type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ads(
        datetime TIMESTAMP,
        utm_source VARCHAR(255),
        utm_campaign VARCHAR(255),
        utm_medium VARCHAR(255),
        cost NUMERIC
);
