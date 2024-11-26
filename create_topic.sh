#!/bin/bash
docker exec kafka kafka-topics --create --topic aquarium_sensors \
  --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1