import {
  Card,
  CardContent,
  Typography,
  Box,
  FormControlLabel,
  TextField,
  MenuItem,
  Checkbox,
  Button,
} from "@mui/material";
import { ChangeEvent, useCallback, useMemo, useState } from "react";
import {
  ConfigRequest,
  defaultConfigValues,
} from "../models/config-request.model";
import {
  binarySelectionTypesOptions,
  realSelectionTypesOptions,
} from "../types/selection-type.type";
import {
  binaryCrossoverTypesOptions,
  realCrossoverTypesOptions,
} from "../types/crossover-type.type";
import {
  binaryMutationTypesOptions,
  realMutationTypesOptions,
} from "../types/mutation-type.type";
import { configLabels } from "../models/config-labels";
import {
  BinaryChromosomeOptionExclusions,
  ChromosomeType,
  RealChromosomeOptionExclusions,
} from "../types/chromosome-type.type";

type FormProps = {
  onSubmit: (form: ConfigRequest) => void;
};

const Form = ({ onSubmit }: FormProps) => {
  const [chromosomeType, setChromosomeType] = useState<ChromosomeType>(() => {
    const savedConfig = localStorage.getItem("config-form");
    return savedConfig ? JSON.parse(savedConfig).chromosome_type : "binary";
  });

  const [form, setForm] = useState<ConfigRequest>(() => {
    const savedConfig = localStorage.getItem("config-form");
    return savedConfig ? JSON.parse(savedConfig) : defaultConfigValues;
  });

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    const isProbability =
      name.includes("probability") || name.includes("proba");
    let parsedValue: number | string | boolean = value;

    if (type === "checkbox") {
      parsedValue = (e.target as HTMLInputElement).checked;
    } else if (type === "number") {
      const numValue = parseFloat(value);
      parsedValue = isProbability
        ? Math.min(Math.max(numValue, 0), 1)
        : numValue;
    }

    setForm((prev) => ({
      ...prev,
      [name]: parsedValue,
    }));
  };

  const handleLocalSubmit = () => {
    localStorage.setItem("config-form", JSON.stringify(form));
    onSubmit(form);
  };

  const handleChromosomeTypeChange = useCallback((newType: ChromosomeType) => {
    setChromosomeType(newType);

    if (newType === "binary") {
      setForm((prev) => ({
        ...prev,
        chromosome_type: newType,
        selection_type: binarySelectionTypesOptions[0],
        crossover_type: binaryCrossoverTypesOptions[0],
        mutation_type: binaryMutationTypesOptions[0],
      }));
    } else {
      setForm((prev) => ({
        ...prev,
        chromosome_type: newType,
        selection_type: realSelectionTypesOptions[0],
        crossover_type: realCrossoverTypesOptions[0],
        mutation_type: realMutationTypesOptions[0],
      }));
    }
  }, []);

  const optionsDict: Record<string, string[]> = useMemo(() => {
    switch (chromosomeType) {
      case "binary":
        return {
          selection_type: binarySelectionTypesOptions,
          crossover_type: binaryCrossoverTypesOptions,
          mutation_type: binaryMutationTypesOptions,
        };
      case "real":
        return {
          selection_type: realSelectionTypesOptions,
          crossover_type: realCrossoverTypesOptions,
          mutation_type: realMutationTypesOptions,
        };
      default:
        return {
          selection_type: [],
          crossover_type: [],
          mutation_type: [],
        };
    }
  }, [chromosomeType]);

  const configExclusions = useMemo(() => {
    switch (chromosomeType) {
      case "binary":
        return BinaryChromosomeOptionExclusions;
      case "real":
        return RealChromosomeOptionExclusions;
      default:
        return [];
    }
  }, [chromosomeType]);

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Parametry algorytmu genetycznego
        </Typography>
        <Box component="form" display="grid" gap={2}>
          <TextField
            select
            label="Typ chromosomu"
            name="chromosome_type"
            value={chromosomeType}
            onChange={(e) =>
              handleChromosomeTypeChange(e.target.value as ChromosomeType)
            }
            fullWidth
          >
            <MenuItem value="binary">Binarny</MenuItem>
            <MenuItem value="real">Rzeczywisty</MenuItem>
          </TextField>
          {Object.entries(defaultConfigValues).map(([key, value]) => {
            if (configExclusions.includes(key as keyof ConfigRequest))
              return "";

            if (typeof value === "boolean") {
              return (
                <FormControlLabel
                  key={configLabels[key as keyof ConfigRequest]}
                  control={
                    <Checkbox
                      checked={form[key as keyof ConfigRequest] as boolean}
                      onChange={handleChange}
                      name={key}
                    />
                  }
                  label={key}
                />
              );
            } else if (typeof value === "number") {
              const isProbability =
                key.includes("probability") || key.includes("proba");
              return (
                <TextField
                  key={key}
                  type="number"
                  label={configLabels[key as keyof ConfigRequest]}
                  name={key}
                  inputProps={{
                    step: "0.01",
                    min: isProbability ? 0 : undefined,
                    max: isProbability ? 1 : undefined,
                  }}
                  value={form[key as keyof ConfigRequest] as number}
                  onChange={handleChange}
                  fullWidth
                />
              );
            } else if (typeof value === "string") {
              const options: string[] =
                optionsDict[key as keyof ConfigRequest] || [];

              return (
                <TextField
                  key={key}
                  select
                  label={configLabels[key as keyof ConfigRequest]}
                  name={key}
                  value={form[key as keyof ConfigRequest] as string}
                  onChange={handleChange}
                  fullWidth
                >
                  {options.map((option) => (
                    <MenuItem key={option} value={option}>
                      {option}
                    </MenuItem>
                  ))}
                </TextField>
              );
            }
            return null;
          })}
          <Button variant="contained" onClick={handleLocalSubmit}>
            Oblicz
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default Form;
