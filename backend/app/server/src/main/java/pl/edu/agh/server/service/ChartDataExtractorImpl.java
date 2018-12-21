package pl.edu.agh.server.service;

import com.google.common.cache.Cache;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import pl.edu.agh.domain.db.entity.Prediction;
import pl.edu.agh.domain.db.repository.PredictionRepository;
import pl.edu.agh.domain.net.chart.ChartData;

import javax.annotation.PostConstruct;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import static com.google.common.cache.CacheBuilder.newBuilder;

@Slf4j
@Service
public class ChartDataExtractorImpl implements ChartDataExtractor<ChartData> {

    private static final String PREDICTIONS_CHART_LABEL = "Predicted volume";
    private static final String HISTORICAL_MIN_VALUES_CHART_LABEL = "Historical min volume";
    private static final String HISTORICAL_MAX_VALUES_LABEL = "Historical max volume";

    private final PredictionRepository predictionRepository;

    @Value("${pl.edu.agh.cache.cachedSensorChartDataSize}")
    private Integer cachedChartDataSize;

    private Cache<Long, List<ChartData>> chartsPerSensor;


    @Autowired
    public ChartDataExtractorImpl(PredictionRepository predictionRepository) {
        this.predictionRepository = predictionRepository;
    }


    @PostConstruct
    public void initCache() {
        if (cachedChartDataSize <= 0) {
            throw new IllegalArgumentException("Property pl.edu.agh.cache.cachedSensorChartData must be greater than 0");
        }

        chartsPerSensor = newBuilder()
                .maximumSize(cachedChartDataSize)
                .expireAfterWrite(2, TimeUnit.MINUTES)
                .build();

    }

    @Override
    public List<ChartData> extractChartData(Long sensorId) {
        try {
            return chartsPerSensor.get(sensorId, () -> getChartData(sensorId));
        } catch (ExecutionException e) {
            log.error(String.format("Problem occurred while trying to extract data for chart with sensor %d", sensorId), e);
        }
        return Collections.emptyList();
    }

    private List<ChartData> getChartData(Long sensorId) {
        List<Prediction> predictions = getPredictions(sensorId);
        Map<LocalDateTime, Integer> minVolumes = predictions.parallelStream().collect(Collectors.toMap(Prediction::getDateTime, Prediction::getMinVolume));
        Map<LocalDateTime, Integer> totalVolumes = predictions.parallelStream().collect(Collectors.toMap(Prediction::getDateTime, Prediction::getTotalVolume));
        Map<LocalDateTime, Integer> maxVolumes = predictions.parallelStream().collect(Collectors.toMap(Prediction::getDateTime, Prediction::getMaxVolume));

        ChartData totalVolumesChart = ChartData.builder().name(PREDICTIONS_CHART_LABEL).values(totalVolumes).build();
        ChartData minVolumesChart = ChartData.builder().name(HISTORICAL_MIN_VALUES_CHART_LABEL).values(minVolumes).build();
        ChartData maxVolumesChart = ChartData.builder().name(HISTORICAL_MAX_VALUES_LABEL).values(maxVolumes).build();
        return Arrays.asList(totalVolumesChart, minVolumesChart, maxVolumesChart);
    }

    private List<Prediction> getPredictions(Long sensorId) {
        return predictionRepository.findAllBySensorId(sensorId);
    }
}
