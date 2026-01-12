CREATE STREAM raw_posts (
    event_type STRING,
    uuid STRING,
    title STRING,
    body STRING,
    timestamp STRING
) WITH (
    KAFKA_TOPIC='posts',
    VALUE_FORMAT='JSON',
    KEY_FORMAT='KAFKA'
    );

