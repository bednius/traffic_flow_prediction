package pl.edu.agh.domain.net;


import lombok.*;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class SensorDTO {
    private String name;
    private Double longitude;
    private Double latitude;
}
