package pl.edu.agh.server.service;

import com.google.common.cache.Cache;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
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
        LocalDateTime dateTime = LocalDateTime.of(2015,11,22,0,0,0);
        LocalDateTime finishDateTime = LocalDateTime.of(2015,12,1,0,0,0);

        List<Measurement> allBySensorId = measurementRepository.findAllBySensorIdByDateTimeAfer(id, dateTime, finishDateTime);
        allBySensorId.parallelStream()
                .forEach(m -> m.setDateTime(m.getDateTime().withYear(2018)));

        Map<LocalDateTime, Integer> values =  allBySensorId.size() > 0 ?
                allBySensorId.parallelStream()
                        .collect(Collectors.toMap(m -> m.getDateTime(), m -> m.getTotalVolume()!= null ? m.getTotalVolume(): 0, (x1,x2) -> x1)):
                Collections.emptyMap();

        Map<LocalDateTime, Integer> velocity =  allBySensorId.size() > 0 ?
                allBySensorId.parallelStream()
                        .collect(Collectors.toMap(m -> m.getDateTime(), m -> m.getAvgMph()!= null ? m.getAvgMph(): 0, (x1,x2) -> x1)):
                Collections.emptyMap();


        ChartData volume = ChartData.builder().name("volume").values(values).build();
        ChartData velocityChart = ChartData.builder().name("mph").values(velocity).build();

        return Arrays.asList(volume, velocityChart);
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
        List<SensorDTO> sensorDTOS = new ArrayList<>(values);

        return sensorDTOS.subList(555,4000);
    }
}
