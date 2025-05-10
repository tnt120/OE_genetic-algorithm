import { ConfigRequest } from "../models/config-request.model";

export type ChromosomeType = "binary" | "real";

export const BinaryChromosomeOptionExclusions: Array<keyof ConfigRequest> =
  [] as const;

export const RealChromosomeOptionExclusions: Array<keyof ConfigRequest> = [
  "inversion_proba",
] as const;
