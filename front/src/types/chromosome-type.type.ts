import { ConfigRequest } from "../models/config-request.model";

export type ChromosomeType = "binary" | "real";

export const BinaryChromosomeOptionExclusions: Array<keyof ConfigRequest> = [
  "chromosome_type",
  "alpha",
  "beta"
] as const;

export const RealChromosomeOptionExclusions: Array<keyof ConfigRequest> = [
  "chromosome_type",
  "inversion_proba",
  "chromosome_length",
  "probability_uniform_crossover"
] as const;
