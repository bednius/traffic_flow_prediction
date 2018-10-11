package pl.edu.agh.downloader.domain.db.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.edu.agh.downloader.domain.db.entity.Measurement;

public interface MeasurementRepository extends JpaRepository<Measurement, Long> {
}
