docker exec -it postgres psql -U postgres -d aquarium_data -c "CREATE TABLE sensor_readings (
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
    overall_status VARCHAR(10)
);"
