package pl.edu.agh.server.service;

import com.google.common.cache.Cache;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import pl.edu.agh.domain.db.entity.Measurement;
import pl.edu.agh.domain.db.entity.Sensor;
import pl.edu.agh.domain.db.repository.MeasurementRepository;
import pl.edu.agh.domain.db.repository.SensorRepository;
import pl.edu.agh.domain.net.SensorDTO;
import pl.edu.agh.domain.net.chart.ChartData;

import javax.annotation.PostConstruct;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static com.google.common.cache.CacheBuilder.*;

@Service
public class PredictionsService implements PredictionsProvider<SensorDTO, ChartData> {

    @Value("${pl.edu.agh.cache.sensors}")
    private Integer sensorCacheSize;

    @Value("${pl.edu.agh.cache.predictions}")
    private Integer predictionsCacheSize;

    private final SensorRepository sensorRepository;
    private final MeasurementRepository measurementRepository;

    private Cache<Long, SensorDTO> sensors;

    @Autowired
    public PredictionsService(SensorRepository sensorRepository, MeasurementRepository measurementRepository) {
        this.sensorRepository = sensorRepository;
        this.measurementRepository = measurementRepository;
    }


    @PostConstruct
    public void initCache(){
        List<Sensor> sensors = sensorRepository.findAll();

        this.sensors = newBuilder()
                .maximumSize(sensorCacheSize <=0 ? sensors.size() : sensorCacheSize)
                .expireAfterAccess(1,TimeUnit.HOURS)
                .build();

        for(Sensor sensor: sensors){
            if(sensor.getLatitude() != null && sensor.getLongitude() != null){
                this.sensors.put(sensor.getId(),SensorDTO.builder()
                        .latitude(sensor.getLatitude())
                        .longitude(sensor.getLongitude())
                        .name(sensor.getId().toString())
                        .build()
                );
            }
        }
    }

    @Override
    public List<ChartData> getPredictionsBySensorId(Long id) {
        List<Measurement> allBySensorId = measurementRepository.findAllBySensorId(id);

        Map<LocalDateTime, Integer> values =  allBySensorId.size() > 0 ?
                allBySensorId.stream().collect(Collectors.toMap(m -> m.getDateTime(), m -> m.getTotalVolume()!= null ? m.getTotalVolume(): 0, (x1,x2) -> x1)):
                Collections.emptyMap();
        return Stream.of(ChartData.builder().name("volume").values(values).build()).collect(Collectors.toList());
    }

    @Override
    public SensorDTO getSensorById(Long id) {
        try {
            return sensors.get(id, () -> sensorRepository.retrieveSensorAsDTO(id));
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public List<SensorDTO> getAllSensor() {
        Collection<SensorDTO> values = sensors.asMap().values();
        return new ArrayList<>(values);
    }
}
