package pl.edu.agh.downloader.task;

import org.apache.commons.httpclient.MultiThreadedHttpConnectionManager;
import org.apache.commons.httpclient.params.HttpConnectionManagerParams;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HttpClientConectionManager {

    @Bean
    public MultiThreadedHttpConnectionManager multiThreadedHttpConnectionManager(HttpConnectionManagerParams params) {
        MultiThreadedHttpConnectionManager multiThreadedHttpConnectionManager = new MultiThreadedHttpConnectionManager();
        multiThreadedHttpConnectionManager.setParams(params);
        return multiThreadedHttpConnectionManager;
    }

    @Bean
    public HttpConnectionManagerParams httpConnectionManagerParams() {
        HttpConnectionManagerParams httpConnectionManagerParams = new HttpConnectionManagerParams();
        return httpConnectionManagerParams;
    }
}