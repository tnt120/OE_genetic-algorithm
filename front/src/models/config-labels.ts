import { ConfigRequest } from './config-request.model';

export const configLabels: Record<keyof ConfigRequest, string> = {
    chromosome_length: 'Długość chromosomu',
    dimensions: 'Liczba wymiarów',
    population_size: 'Rozmiar populacji',
    epochs: 'Liczba epok',
    probability_uniform_crossover: 'Prawdopodobieństwo uniform crossover',
    probability_mutation: 'Prawdopodobieństwo mutacji',
    probability_crossover: 'Prawdopodobieństwo krzyżowania',
    selection_type: 'Typ selekcji',
    crossover_type: 'Typ krżyżowania',
    mutation_type: 'Typ mutacji',
    elitism: 'Elityzm',
    inversion_proba: 'Prawdopodobieństwo inwersji',
};
