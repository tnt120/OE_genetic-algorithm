import { Card, CardContent, Typography, Box, FormControlLabel, TextField, MenuItem, Checkbox, Button } from '@mui/material';
import { ChangeEvent, useState } from 'react';
import { ConfigRequest, defaultConfigValues } from '../models/config-request.model';
import { selectionTypesOptions } from '../types/selection-type.type';
import { crossoverTypesOptions } from '../types/crossover-type.type';
import { mutationTypesOptions } from '../types/mutation-type.type';
import { configLabels } from '../models/config-labels';

type FormProps = {
    onSubmit: (form: ConfigRequest) => void;
};

const Form = ({ onSubmit }: FormProps) => {
    const [form, setForm] = useState<ConfigRequest>(() => {
        const savedConfig = localStorage.getItem('config-form');
        return savedConfig ? JSON.parse(savedConfig) : defaultConfigValues;
    });

    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value, type } = e.target;
        const isProbability = name.includes('probability') || name.includes('proba');
        let parsedValue: number | string | boolean = value;

        if (type === 'checkbox') {
            parsedValue = (e.target as HTMLInputElement).checked;
        } else if (type === 'number') {
            const numValue = parseFloat(value);
            parsedValue = isProbability ? Math.min(Math.max(numValue, 0), 1) : numValue;
        }

        setForm(prev => ({
            ...prev,
            [name]: parsedValue,
        }));
    };

    const handleLocalSubmit = () => {
        localStorage.setItem('config-form', JSON.stringify(form));
        onSubmit(form);
    };

    return (
        <Card>
            <CardContent>
                <Typography variant="h5" gutterBottom>
                    Parametry algorytmu genetycznego
                </Typography>
                <Box component="form" display="grid" gap={2}>
                    {Object.entries(defaultConfigValues).map(([key, value]) => {
                        if (typeof value === 'boolean') {
                            return (
                                <FormControlLabel
                                    key={configLabels[key as keyof ConfigRequest]}
                                    control={<Checkbox checked={form[key as keyof ConfigRequest] as boolean} onChange={handleChange} name={key} />}
                                    label={key}
                                />
                            );
                        } else if (typeof value === 'number') {
                            const isProbability = key.includes('probability') || key.includes('proba');
                            return (
                                <TextField
                                    key={key}
                                    type="number"
                                    label={configLabels[key as keyof ConfigRequest]}
                                    name={key}
                                    inputProps={{ step: '0.01', min: isProbability ? 0 : undefined, max: isProbability ? 1 : undefined }}
                                    value={form[key as keyof ConfigRequest] as number}
                                    onChange={handleChange}
                                    fullWidth
                                />
                            );
                        } else if (typeof value === 'string') {
                            let options: string[] = [];
                            if (key === 'selection_type') options = selectionTypesOptions;
                            if (key === 'crossover_type') options = crossoverTypesOptions;
                            if (key === 'mutation_type') options = mutationTypesOptions;
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
                                    {options.map(option => (
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
