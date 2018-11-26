package pl.edu.agh.domain.net.download;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class ApiResponse {

    @JsonProperty(value = "Header")
    private Header header;

    @JsonProperty(value = "Rows")
    private List<RowMeasurement> rows;
}
