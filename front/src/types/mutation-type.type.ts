export type MutationType =
  | "edge"
  | "one_point"
  | "two_point"
  | "uniform"
  | "gaussian";

export const binaryMutationTypesOptions: MutationType[] = [
  "edge",
  "one_point",
  "two_point",
];

export const realMutationTypesOptions: MutationType[] = ["uniform", "gaussian"];
