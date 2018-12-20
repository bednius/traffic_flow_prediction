package pl.edu.agh.domain.net.mapper.dto;

import org.springframework.stereotype.Component;
import pl.edu.agh.domain.db.entity.Sensor;
import pl.edu.agh.domain.net.SensorDTO;

@Component
public class SensorToSensorDTOMapper implements MapperToDTO<Sensor, SensorDTO> {

    @Override
    public SensorDTO mapToDTO(Sensor sensor) {
        return SensorDTO.builder()
                .latitude(sensor.getLatitude())
                .longitude(sensor.getLongitude())
                .name(sensor.getId().toString())
                .build();
    }
}
