package pl.edu.agh.downloader.task;

import org.springframework.beans.factory.annotation.Autowired;
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

    @Override
    public void run(String... args) throws Exception {
        int firstSensorId=1,  lastSensorId=18000;
        int threadCount = 3;
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
}
