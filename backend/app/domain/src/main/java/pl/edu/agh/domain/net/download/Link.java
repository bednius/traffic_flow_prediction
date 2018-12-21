package pl.edu.agh.domain.net.download;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.*;

@JsonIgnoreProperties(ignoreUnknown = true)
@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Link {
    private String href;
    private String rel;
}
