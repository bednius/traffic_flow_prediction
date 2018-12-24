# traffic_flow_prediction

Repozytorium pracy inżynierskiej pt. "Przewidywanie natężenia ruchu ulicznego".

Autorzy: Michał Grzesik, Barłomiej Pyjor
Opiekun pracy: dr inż. Marcin Orchel

## Guide
To run project we need database with stored predictions. Firtsly we need to create database with granted user. All instructions were executed on Fedora-based system.

### Create database
Firstly we have to install PostgreSQL server. To be sure whether PostgreSQL was installed correctly, just type
```bash
systemctl status postgresql
```

The expected resutlt is long info listing with line:
```bash
Active: active (running)
```

Then create database with granted user in psql terminal mode:
```bash
   CREATE DATABASE traffic_flow_prediction;
   CREATE USER tfp_user WITH ENCRYPTED PASSWORD 'password@1234' LOGIN NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;
   GRANT ALL PRIVILEGES ON DATABASE traffic_flow_prediction TO tfp_user;
```
### Download data from API
We use data from http://webtris.highwaysengland.co.uk/api/swagger/ui/index. In application.properties file from downloader module you can set range of downloaded sensors, number of threads being executed, and date range of data measurement.

Sample configuration
```java
pl.edu.agh.threadExecutionNumber=4
pl.edu.agh.firstSensorId=1
pl.edu.agh.lastSensorId=20000
pl.edu.agh.measurementStartDate=2016-01-22
pl.edu.agh.measurementFinishDate=2016-03-23
```

Then execute following commands (from downloader directory)

```bash
   maven install;
   java -jar target/downloader-1.0-SNAPSHOT.jar
```
### Run web application
Check whether database connection properties are correct in application.properties in server module
To run server locally type in "server" directory:

```bash
   maven install;
   java -jar target/server-1.0-SNAPSHOT.jar
```
By default, application is run in http://localhost:8080 address.

### Run prediction module
Check if database config is proper(db.cfg).
Then run python script:
```python
   python3 <firstSensorId> <lastSensorId> <startDate> <endDate>
```
Where sensorIds are values between 1 and 17000.
Dates are in format YYYY-MM-DD, example: 2016-02-02.
If necessary install required dependencies.
