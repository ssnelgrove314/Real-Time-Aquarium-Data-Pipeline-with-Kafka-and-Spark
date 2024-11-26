docker exec -it postgres psql -U postgres -d aquarium_data -c "
DROP TABLE IF EXISTS sensor_readings;
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT,
    tds FLOAT,
    ph FLOAT,
    nitrate FLOAT,
    ammonia FLOAT,
    nitrite FLOAT,
    gh FLOAT,
    kh FLOAT,
    temperature_alert VARCHAR(10),
    tds_alert VARCHAR(10),
    ph_alert VARCHAR(10),
    nitrate_alert VARCHAR(10),
    ammonia_alert VARCHAR(10),
    nitrite_alert VARCHAR(10),
    gh_alert VARCHAR(10),
    kh_alert VARCHAR(10),
    overall_status VARCHAR(10)
);"
