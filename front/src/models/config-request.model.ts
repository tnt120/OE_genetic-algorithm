import { CrossoverType } from "../types/crossover-type.type";
import { MutationType } from "../types/mutation-type.type";
import { SelectionType } from "../types/selection-type.type";

export interface ConfigRequest {
  chromosome_type: "binary" | "real";
  chromosome_length: number;
  dimensions: number;
  population_size: number;
  epochs: number;
  probability_uniform_crossover: number;
  probability_mutation: number;
  probability_crossover: number;
  selection_type: SelectionType;
  crossover_type: CrossoverType;
  mutation_type: MutationType;
  elitism: boolean;
  inversion_proba: number;
  alpha: number;
  beta: number;
}

export const defaultConfigValues: ConfigRequest = {
  chromosome_type: "binary",
  chromosome_length: 16,
  dimensions: 2,
  population_size: 16,
  epochs: 1000,
  probability_uniform_crossover: 0.5,
  probability_mutation: 0.5,
  probability_crossover: 0.9,
  selection_type: "best",
  crossover_type: "uniform",
  mutation_type: "two_point",
  elitism: true,
  inversion_proba: 1,
  alpha: 0.3,
  beta: 0.5
};
