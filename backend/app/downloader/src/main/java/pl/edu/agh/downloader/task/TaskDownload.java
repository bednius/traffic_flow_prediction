package pl.edu.agh.downloader.task;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;

@Component
public class TaskDownload implements CommandLineRunner{

    private final DataDownloader dataDownloader;

    @Autowired
    public TaskDownload(DataDownloader dataDownloader) {
        this.dataDownloader = dataDownloader;
    }

    @Value("${pl.edu.agh.firstSensorId}")
    private Integer firstSensorId;

    @Value("${pl.edu.agh.lastSensorId}")
    private Integer lastSensorId;

    @Value("${pl.edu.agh.threadExecutionNumber}")
    private Integer threadCount;


    @Override
    public void run(String... args) throws Exception {
        run(firstSensorId, lastSensorId);
    }

    public void run(Integer firstSensorId, Integer lastSensorId) throws Exception {
        parseValues(firstSensorId, lastSensorId);
        dataDownloader.downloadSensors(firstSensorId, lastSensorId);

        int range = (lastSensorId - firstSensorId) / threadCount;
        int first,last = lastSensorId;

        for (int i = 0; i < threadCount; i++) {
            first = firstSensorId + i *range;
            last = firstSensorId + (i+1) *range;
            dataDownloader.download(first, last);
        }

        if(last < lastSensorId){
            dataDownloader.download(last, lastSensorId);
        }

    }

    private void parseValues(Integer firstSensorId, Integer lastSensorId) {
        if(firstSensorId == null){
            throw new IllegalArgumentException("Property pl.edu.agh.firstSensorId cannot be null");
        }
        if(lastSensorId== null){
            throw new IllegalArgumentException("Property pl.edu.agh.lastSensorId cannot be null");
        }
        if (firstSensorId > lastSensorId){
            throw new IllegalArgumentException("First sensor id cannot be greater than last sensor id");
        }
    }
}
