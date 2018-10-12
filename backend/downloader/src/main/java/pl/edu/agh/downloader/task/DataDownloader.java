package pl.edu.agh.downloader.task;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpException;
import org.apache.commons.httpclient.HttpStatus;
import org.apache.commons.httpclient.MultiThreadedHttpConnectionManager;
import org.apache.commons.httpclient.methods.GetMethod;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.stereotype.Component;
import pl.edu.agh.downloader.domain.db.entity.Measurement;
import pl.edu.agh.downloader.domain.db.entity.Sensor;
import pl.edu.agh.downloader.domain.db.repository.MeasurementRepository;
import pl.edu.agh.downloader.domain.db.repository.SensorRepository;
import pl.edu.agh.downloader.domain.net.ApiResponse;
import pl.edu.agh.downloader.domain.net.Link;
import pl.edu.agh.downloader.domain.net.RowMeasurement;

import javax.annotation.PostConstruct;
import javax.persistence.EntityManager;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Slf4j
@Component
public class DataDownloader {

    private static final String DATA_SERVER_ADDRESS = "http://webtris.highwaysengland.co.uk/api/v1/reports/01012015/to/31122015/daily?sites=%s&page=1&page_size=2000";

    private final MultiThreadedHttpConnectionManager httpConnectionManager;
    private final ObjectMapper objectMapper;
    private final SensorRepository sensorRepository;
    private final MeasurementRepository measurementRepository;
    DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss");
    DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss");


    @Autowired
    public DataDownloader(MultiThreadedHttpConnectionManager httpConnectionManager, ObjectMapper objectMapper, SensorRepository sensorRepository, MeasurementRepository measurementRepository) {
        this.httpConnectionManager = httpConnectionManager;
        this.objectMapper = objectMapper;
        this.sensorRepository = sensorRepository;
        this.measurementRepository = measurementRepository;
    }


    @Async
    public void download(int firstSensorId, int lastSensorId) {
        log.info(String.format("*Init task -  downloading data for range: <%d, %d)  .", firstSensorId, lastSensorId));

        HttpClient client = new HttpClient(httpConnectionManager);
        String res;
        GetMethod get = new GetMethod(String.format(DATA_SERVER_ADDRESS, String.valueOf(1)));
        for (int id = firstSensorId; id < lastSensorId; id++) {
            try {

                get = new GetMethod(String.format(DATA_SERVER_ADDRESS, String.valueOf(id)));

                ApiResponse apiResponse;
                String nextAddress;
                log.info("*Downloading data from server has been started for sensor=." + id);
                do {
                    int statusCode = client.executeMethod(get);
                    if (statusCode != HttpStatus.SC_OK) {
                        log.error("Method failed: " + get.getStatusLine() + "for sensor_id: " + String.valueOf(id) + "with status: " + statusCode);
                        break;

                    } else {
                        res = get.getResponseBodyAsString();
                        apiResponse = objectMapper.readValue(res, ApiResponse.class);
                        log.info(apiResponse.toString());
                        persistObjectToDb(apiResponse, id);
                    }
                    nextAddress = getNextAddress(apiResponse);
                    log.debug("Next link is = " + nextAddress);

                    get = new GetMethod(nextAddress);
                } while (nextAddress != null);


            } catch (HttpException e) {
                log.error("Fatal protocol violation: " + e.getMessage());
                e.printStackTrace();
            } catch (IOException e) {
                log.error(e.getMessage());
                e.printStackTrace();
            } finally {
                get.releaseConnection();

            }

        }
        log.info(String.format("*Finished downloading data for range : <%d, %d)", firstSensorId, lastSensorId));

    }

    private String getNextAddress(ApiResponse apiResponse) {
        for (Link link : apiResponse.getHeader().getLinks()) {
            if (link.getRel().equals("nextPage")) {
                return link.getHref();
            }
        }
        return null;
    }

    private void persistObjectToDb(ApiResponse apiResponse, long id) {
        Optional<Sensor> sensorOpt;
        Sensor sensor;
        if (apiResponse.getRows().size() > 0) {
            sensorOpt = sensorRepository.findById(id);


            if (!sensorOpt.isPresent()) {
                sensor = Sensor.builder().id(id).name(apiResponse.getRows().get(0).getSensorName()).build();
                sensorRepository.save(sensor);
            } else {
                sensor = sensorOpt.get();
            }
        } else {
            return;
        }

        List<Measurement> measurements = new ArrayList<>(apiResponse.getRows().size());
        for (RowMeasurement row : apiResponse.getRows()) {
            Measurement measurement = Measurement.builder()
                    .avgMph(row.getAvgMph())
                    .dateTime(LocalDateTime.of(LocalDateTime.parse(row.getMeasurementDate(), dateTimeFormatter).toLocalDate(), LocalTime.parse(row.getTimeOfMeasurement(), timeFormatter)))
                    .status(row.getAvgMph() != null && row.getAvgMph() > 0 ? "SUCCESSFUL" : "NO_DATA")
                    .sensor(sensor)
                    .totalVolume(row.getTotalVolume())
                    .build();
            measurements.add(measurement);
        }
        measurementRepository.saveAll(measurements);
    }
}
