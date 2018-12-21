package pl.edu.agh.domain.db.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.DynamicInsert;
import org.hibernate.annotations.DynamicUpdate;

import javax.persistence.*;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
@DynamicUpdate
@DynamicInsert
@Entity
public class Sensor {

    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
    @Column(name = "id", updatable = false)
    private Long id;

    private String name;

    private Double longitude;

    private Double latitude;
}
