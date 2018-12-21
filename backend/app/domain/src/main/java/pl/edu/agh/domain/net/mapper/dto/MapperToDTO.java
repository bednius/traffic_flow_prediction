package pl.edu.agh.domain.net.mapper.dto;

public interface MapperToDTO<D, T> {
    T mapToDTO(D object);
}
