package pl.edu.agh.server;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        Map<LocalDateTime, Integer> map = new HashMap<>();
        map.put(LocalDateTime.now().plusDays(1), 1);
        map.put(LocalDateTime.now().plusDays(2), 2);
        map.put(LocalDateTime.now().plusDays(3), 3);
        map.put(LocalDateTime.now().plusDays(4), 4);

        System.out.println(        objectMapper.writeValueAsString(map));
    }
}
