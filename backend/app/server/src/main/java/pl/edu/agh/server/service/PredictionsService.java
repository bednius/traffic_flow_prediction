package pl.edu.agh.server.service;

import com.google.common.cache.Cache;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import pl.edu.agh.domain.db.entity.Sensor;
import pl.edu.agh.domain.db.repository.PredictionRepository;
import pl.edu.agh.domain.db.repository.SensorRepository;
import pl.edu.agh.domain.net.SensorDTO;
import pl.edu.agh.domain.net.chart.ChartData;

import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.concurrent.ExecutionException;

import static com.google.common.cache.CacheBuilder.newBuilder;

@Service
@Slf4j
public class PredictionsService implements PredictionsProvider<SensorDTO, ChartData> {

    @Value("${pl.edu.agh.cache.sensors}")
    private Integer sensorCacheSize;

    private final SensorRepository sensorRepository;
    private final ChartDataExtractor<ChartData> chartDataExtractor;


    private Cache<Long, SensorDTO> sensors;

    @Autowired
    public PredictionsService(SensorRepository sensorRepository, PredictionRepository predictionRepository, ChartDataExtractor<ChartData> chartDataExtractor) {
        this.sensorRepository = sensorRepository;
        this.chartDataExtractor = chartDataExtractor;
    }


    @PostConstruct
    public void initCache(){
        List<Sensor> sensors = sensorRepository.findSensorsWithPredictions();

        this.sensors = newBuilder()
                .maximumSize(sensorCacheSize <= 0 ? sensorRepository.count() : sensorCacheSize)
                .build();

        for(Sensor sensor: sensors){
                this.sensors.put(sensor.getId(),SensorDTO.builder()
                        .latitude(sensor.getLatitude())
                        .longitude(sensor.getLongitude())
                        .name(sensor.getId().toString())
                        .build()
                );
        }
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
