package pl.edu.agh.server.service;

import pl.edu.agh.domain.net.SensorDTO;
import pl.edu.agh.domain.net.chart.ChartData;

import java.util.List;

public interface PredictionsProvider<D extends SensorDTO,T extends ChartData> {

    List<T> getPredictionsBySensorId(Long id);

    D getSensorById(Long id);

    List<D> getAllSensor();
}
