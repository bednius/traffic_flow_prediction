package pl.edu.agh.domain.db.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import pl.edu.agh.domain.db.entity.Prediction;

import java.math.BigInteger;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface PredictionRepository extends JpaRepository<Prediction, Long> {

    @Query(value = "SELECT * FROM PREDICTION WHERE sensor_object_id = ?1", nativeQuery = true)
    List<Prediction> findAllBySensorId(Long id);

    @Query(value = "SELECT * FROM PREDICTION WHERE sensor_object_id = ?1 and datetime >= ?2 and datetime <= ?3", nativeQuery = true)
    List<Prediction> findAllBySensorIdByDateTimeAfer(Long id, LocalDateTime startDateTime, LocalDateTime finishDateTime);

    @Query(value ="SELECT sensor_object_id FROM PREDICTION p GROUP BY sensor_object_id", nativeQuery = true)
    List<BigInteger> findSensorsWithPrediction();
}