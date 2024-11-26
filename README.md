# Real-Time-Aquarium-Data-Pipeline-with-Kafka-and-Spark
Create a real-time data pipeline that simulates IoT sensor data for aquariums, processes it with Apache Spark, stores it in PostgreSQL and visualizes the data with streamlit.

# Setup
Run on Ubuntu
Must have docker and docker-compose installed

run the following commands in order
`docker-compose up -d`
`pip install requirements.txt`
`bash create_topic.sh`
`bash create_table.sh`
`python kafka_producer.py &> kafka_producer.log &`
`python spark_consumer.py &> spark_consumer.log &`
`bash run_vis.sh`

click on the Local URL to view the visualization
Press R to rerun the vis to see the newly inputed data

# Additional Info
The data generated isn't the most acurate simulation of sensor data in an aquarium, so the plots might look a little chaotic compared to what you would expect acutal sensor data to look.

The log files will have the output of the running kafka_producer and spark_consumer if you wish to view them.

You can also run `bash show_table_data_in_postgres.sh` to view the raw table data in postgres.

The Data Overview will only have the first 1000 results to view and export.

This was only tested in a github codespace environment (Ubuntu). Other environments might work but might have slightly different requirements.

# Shutdown
To stop the background processes after you are done, run `kill $(jobs -p)`

To stop running docker containers run `docker-compose down`

# TODO
* Modify the generate_data.py script to create more accurate simulated data. Also have it occasionally generate data that goes above the alerting threshold.
* Add rolling window aggregates to spark_consumer.py
* Improve streamlit visualization
* Add multiple aquariums
* Add devcontainer.json to make it easier to run on multiple systems