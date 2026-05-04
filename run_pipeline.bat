@echo off

echo Starting Data Pipeline...

echo Cleaning old containers...
docker-compose down -v

echo Starting containers...
docker-compose up -d

echo Waiting for Kafka...
:waitKafka
docker exec kafka kafka-topics --bootstrap-server kafka:9092 --list >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    timeout /t 5 >nul
    goto waitKafka
)
echo Kafka is ready

echo Waiting for MySQL (fully ready)...

:waitMySQLReady
docker exec mysql mysql -uroot -proot -e "SELECT 1" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    timeout /t 5 >nul
    goto waitMySQLReady
)

echo MySQL is fully ready

echo Creating MySQL table...
docker exec mysql mysql -uroot -proot -e "USE orders_db; CREATE TABLE IF NOT EXISTS orders (order_id INT, customer VARCHAR(255), location VARCHAR(255), status VARCHAR(50), timestamp VARCHAR(50), price_factor DOUBLE, weather VARCHAR(50), delay INT);"

echo Creating Kafka topic...
docker exec kafka kafka-topics --create --if-not-exists --topic orders_topic --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1

echo Creating MySQL table...
docker exec -i mysql mysql -uroot -proot -e "USE orders_db; CREATE TABLE IF NOT EXISTS orders (order_id INT, customer VARCHAR(255), location VARCHAR(255), status VARCHAR(50), timestamp VARCHAR(50), price_factor DOUBLE, weather VARCHAR(50), delay INT);"

echo Starting Spark job...
docker exec -d spark spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,mysql:mysql-connector-java:8.0.33 /opt/spark-apps/consumer_spark.py

echo Starting Producer...
start cmd /k python producer.py

echo.
echo PIPELINE IS LIVE!
echo Kafka UI: http://localhost:8085