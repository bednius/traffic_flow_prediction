package pl.edu.agh.domain.net.download;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDateTime;
import java.time.LocalTime;


@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RowMeasurement {
    @JsonProperty(value = "Site Name")
    private String sensorName;

    @JsonProperty(value = "Report Date")
//    @JsonFormat(pattern = "yyyy-MM-ddTHH:mm:ss")
    private String measurementDate;

    @JsonProperty(value = "Time Period Ending")
    private String timeOfMeasurement;

    @JsonProperty(value = "Avg mph")
    private Integer avgMph;

    @JsonProperty(value = "Total Volume")
    private Integer totalVolume;

}
