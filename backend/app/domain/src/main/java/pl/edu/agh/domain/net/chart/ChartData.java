package pl.edu.agh.domain.net.chart;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.time.LocalDateTime;
import java.util.Map;


@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class ChartData {
    private String name;

    @JsonProperty("data")
    private Map<LocalDateTime, Integer> values;
}
