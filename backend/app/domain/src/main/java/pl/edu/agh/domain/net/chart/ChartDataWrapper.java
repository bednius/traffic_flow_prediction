package pl.edu.agh.domain.net.chart;

import lombok.*;

import java.util.List;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class ChartDataWrapper {
    private List<ChartData> data;
}
