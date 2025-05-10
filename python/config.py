from dataclasses import dataclass


@dataclass
class Config:
    chromosome_length: int = 16
    variable_range: tuple[float, float] = (-5.0, 5.0)
    dimensions: int = 2

    population_size: int = 16
    epochs: int = 10000

    probability_uniform_crossover: float = 0.5
    probability_mutation: float = 0.1
    probability_crossover: float = 0.9

    selection_type: str = "roulette"  # "best", "roulette", "tournament"
    crossover_type: str = "arithmetic"  # "single_point", "two_point", "uniform", "grain", "arithmetic", "linear", "alpha_blend", "alpha_beta_blend", "average"
    mutation_type: str = "uniform"  # "edge", "one_point", "two_point", "uniform", "gaussian"
    elitism: bool = True
    inversion_proba: float = 0.5

    chromosome_type: str = "real"  # or "real"

    alpha: float = 0.3
    beta: float = 0.5

    @staticmethod
    def from_request(request) -> "Config":
        if request is None:
            return Config()
        config = Config(**{
            k: v
            for k, v in request.items() if k in Config.__annotations__
        })
        return config


GENES = [
    '00011100000101111001110011010110', '01000000011111111110010101000100',
    '10110111001011011111111101101001', '11010110001010001110000111001100',
    '00001010010011000010010001011000', '10000110100100000010001001111100',
    '00100011010001101010101111101010', '00101000000100000011101100101010',
    '00100011000001110110100011000001', '01110010100101101100101100111101',
    '11111111011011110011010101011111', '01011110010110010001111000101100',
    '11111101001011101110001110110100', '10100010000110010011110011110001',
    '11001101100110110001111000011010', '00101101111000001100111001001000'
]
