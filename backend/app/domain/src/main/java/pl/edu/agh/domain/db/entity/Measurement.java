package pl.edu.agh.domain.db.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.DynamicInsert;
import org.hibernate.annotations.DynamicUpdate;

import javax.persistence.*;
import java.time.LocalDateTime;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
@DynamicUpdate
@DynamicInsert
@Entity
@Table(indexes = {
        @Index(name = "measurement_sensor_object_index", columnList = "sensor_object_id", unique = false),
        @Index(name = "measurement_datetime_index", columnList = "datetime", unique = false),
        @Index(name = "measurement_sensor_object_datetime_unique_index", columnList = "sensor_object_id,datetime", unique = true)})

public class Measurement {

    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    @Column(name = "id", updatable = false)
    private Long id;

    @Column(name = "datetime")
    private LocalDateTime dateTime;

    @Column(name = "avg_mph")
    private Integer avgMph;

    @Column(name = "total_volume")
    private Integer totalVolume;

    @Enumerated(EnumType.STRING)
    private DownloadStatus status;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "sensor_object_id")
    private Sensor sensor;
}
