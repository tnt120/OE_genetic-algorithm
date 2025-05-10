export type CrossoverType =
  | "single_point"
  | "two_point"
  | "uniform"
  | "grain"
  | "arithmetic"
  | "linear"
  | "alpha_blend"
  | "alpha_beta_blend"
  | "average";

export const binaryCrossoverTypesOptions: CrossoverType[] = [
  "single_point",
  "two_point",
  "uniform",
  "grain",
];

export const realCrossoverTypesOptions: CrossoverType[] = [
  "arithmetic",
  "linear",
  "alpha_blend",
  "alpha_beta_blend",
  "average",
];
