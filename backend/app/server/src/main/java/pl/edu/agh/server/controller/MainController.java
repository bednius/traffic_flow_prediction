package pl.edu.agh.server.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import pl.edu.agh.domain.net.SensorDTO;
import pl.edu.agh.domain.net.chart.ChartData;
import pl.edu.agh.server.service.PredictionsProvider;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Controller
public class MainController {

    private final PredictionsProvider <SensorDTO,ChartData> predictionsProvider;

    @Autowired
    public MainController(PredictionsProvider <SensorDTO,ChartData> predictionsProvider) {
        this.predictionsProvider = predictionsProvider;
    }

    @GetMapping("/")
    public String home(Model model){
        List<SensorDTO> allSensor = predictionsProvider.getAllSensor();
        model.addAttribute("sensors", allSensor);
        return "home";

    }

    @GetMapping("/results/{id}")
    public String result(Model model, @PathVariable Long id) {
        model.addAttribute("chartData", predictionsProvider.getPredictionsBySensorId(id));
        return "chart";

    }
}
