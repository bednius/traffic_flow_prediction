package pl.edu.agh.server.service;

import com.google.common.cache.Cache;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import pl.edu.agh.domain.db.entity.Sensor;
import pl.edu.agh.domain.db.repository.SensorRepository;
import pl.edu.agh.domain.net.SensorDTO;
import pl.edu.agh.domain.net.chart.ChartData;
import pl.edu.agh.domain.net.mapper.dto.MapperToDTO;

import javax.annotation.PostConstruct;
import java.util.*;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

import static com.google.common.cache.CacheBuilder.newBuilder;

@Service
@Slf4j
public class PredictionsService implements PredictionsProvider<SensorDTO, ChartData> {

    @Value("${pl.edu.agh.cache.sensors}")
    private Integer sensorCacheSize;

    private final SensorRepository sensorRepository;
    private final ChartDataExtractor<ChartData> chartDataExtractor;
    private final MapperToDTO<Sensor, SensorDTO> mapperToSensorDTO;

    private Cache<Long, SensorDTO> sensors;

    @Autowired
    public PredictionsService(SensorRepository sensorRepository, ChartDataExtractor<ChartData> chartDataExtractor,
                              MapperToDTO<Sensor, SensorDTO> mapperToSensorDTO) {
        this.sensorRepository = sensorRepository;
        this.chartDataExtractor = chartDataExtractor;
        this.mapperToSensorDTO = mapperToSensorDTO;
    }


    @PostConstruct
    public void initCache() {
        List<Sensor> sensors = sensorRepository.findSensorsWithPredictions();

        this.sensors = newBuilder()
                .maximumSize(sensorCacheSize <= 0 ? sensorRepository.count() : sensorCacheSize)
                .build();

        sensors.forEach(sensor -> this.sensors.put(sensor.getId(), mapperToSensorDTO.mapToDTO(sensor)));
    }

    @Scheduled(fixedRate = 24 * 60 * 1000, initialDelay = 5000)
    private void refreshSensorCache() {
        log.info("SENSOR CACHE - Started to refresh");

        List<Sensor> sensorsWithPredictions = sensorRepository.findSensorsWithPredictions();
        Map<Long, Sensor> mapSensor = sensorsWithPredictions.parallelStream().collect(Collectors.toMap(Sensor::getId, s -> s));

        Set<Long> storedIdsSensors = this.sensors.asMap().keySet();
        storedIdsSensors.forEach(s -> {
            if (!mapSensor.containsKey(s)) {
                this.sensors.invalidate(s);
            } else {
                this.sensors.put(s, mapperToSensorDTO.mapToDTO(mapSensor.get(s)));
            }
        });

        log.info("SENSOR CACHE - Finish refreshing");
    }


    @Override
    public List<ChartData> getPredictionsBySensorId(Long id) {
        return chartDataExtractor.extractChartData(id);
    }


    @Override
    public SensorDTO getSensorById(Long id) {
        try {
            return sensors.get(id, () -> sensorRepository.retrieveSensorAsDTO(id));
        } catch (ExecutionException e) {
            log.warn(String.format("Failed to find sensor for sensor id = %d", id), e);
        }
        return null;
    }

    @Override
    public List<SensorDTO> getAllSensor() {
        Collection<SensorDTO> values = sensors.asMap().values();
        return new ArrayList<>(values);
    }
}
