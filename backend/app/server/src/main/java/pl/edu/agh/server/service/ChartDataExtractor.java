package pl.edu.agh.server.service;

import pl.edu.agh.domain.net.chart.ChartData;

import java.util.List;

public interface ChartDataExtractor<T extends ChartData> {

    List<T> extractChartData(Long sensorId);

}
