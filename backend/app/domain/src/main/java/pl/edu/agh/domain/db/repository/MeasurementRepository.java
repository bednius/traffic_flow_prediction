package pl.edu.agh.domain.db.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import pl.edu.agh.domain.db.entity.Measurement;

import java.util.List;

@Repository
public interface MeasurementRepository extends JpaRepository<Measurement, Long> {

//    @Query("from Review r inner join fetch r.comments where r.reviewId = :id")
//    User findByReviewId(@Param("id") int id);

    @Query(value = "SELECT * FROM MEASUREMENT WHERE sensor_object_id = ?1", nativeQuery = true)
    List<Measurement> findAllBySensorId(Long id);
}
