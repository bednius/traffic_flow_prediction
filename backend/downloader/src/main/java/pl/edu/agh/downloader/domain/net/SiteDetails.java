package pl.edu.agh.downloader.domain.net;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SiteDetails {

    @JsonProperty("Id")
    private String id;

    @JsonProperty("Name")
    private String name;

    @JsonProperty("Description")
    private String description;

    @JsonProperty("Status")
    private String status;

    @JsonProperty("Longitude")
    private Double longitude;

    @JsonProperty("Latitude")
    private Double latitude;
}
