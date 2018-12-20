package pl.edu.agh.domain.net.download;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;


@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RowMeasurement {
    @JsonProperty(value = "Site Name")
    private String sensorName;

    @JsonProperty(value = "Report Date")
    private String measurementDate;

    @JsonProperty(value = "Time Period Ending")
    private String timeOfMeasurement;

    @JsonProperty(value = "Avg mph")
    private Integer avgMph;

    @JsonProperty(value = "Total Volume")
    private Integer totalVolume;

}
