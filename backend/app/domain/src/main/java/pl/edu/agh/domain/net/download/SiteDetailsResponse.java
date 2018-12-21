package pl.edu.agh.domain.net.download;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SiteDetailsResponse {

    @JsonProperty("row_count")
    private int rowCount;

    @JsonProperty("sites")
    private List<SiteDetails> sites;

}
