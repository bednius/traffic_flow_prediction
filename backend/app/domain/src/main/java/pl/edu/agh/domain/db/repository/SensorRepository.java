package pl.edu.agh.domain.db.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import pl.edu.agh.domain.db.entity.Prediction;
import pl.edu.agh.domain.db.entity.Sensor;
import pl.edu.agh.domain.net.SensorDTO;

import java.util.Collection;
import java.util.List;

@Repository
public interface SensorRepository extends JpaRepository<Sensor, Long> {

    @Query("SELECT new pl.edu.agh.domain.net.SensorDTO(s.name, s.longitude, s.latitude) FROM Sensor s where s.id = ?1")
    SensorDTO retrieveSensorAsDTO(Long id);

    @Query(value = "select sensor.id, sensor.name, sensor.latitude, sensor.longitude from sensor join prediction on  " +
            "sensor.id = prediction.sensor_object_id group by (sensor.id, sensor.name, sensor.latitude, sensor.longitude )", nativeQuery = true)
    List<Sensor> findSensorsWithPredictions();

    List<Sensor> findByIdIn(List<Long> ids);
}
