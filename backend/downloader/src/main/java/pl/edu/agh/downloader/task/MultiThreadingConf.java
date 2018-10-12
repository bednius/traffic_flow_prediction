package pl.edu.agh.downloader.task;

import lombok.extern.log4j.Log4j;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
@Slf4j
public class MultiThreadingConf {

    public Executor asyncExecutor() {
        ThreadPoolTaskExecutor threadPoolTaskExecutor = new ThreadPoolTaskExecutor();
        threadPoolTaskExecutor.setCorePoolSize(3);
        threadPoolTaskExecutor.setMaxPoolSize(20);
        threadPoolTaskExecutor.setThreadNamePrefix("MyExecutor-");
        threadPoolTaskExecutor.initialize();
        log.info("ASYNC CONFIGURED");
        return threadPoolTaskExecutor;
    }
}
