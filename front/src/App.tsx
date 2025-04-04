import { useState } from 'react';
import axios from 'axios';
import { CircularProgress, Typography, Box } from '@mui/material';
import { ConfigRequest } from './models/config-request.model';
import Result from './components/Result';
import { GenericAlgorithmResponse } from './models/generic-algorithm-response.model';
import Form from './components/Form';

export default function App() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<GenericAlgorithmResponse | null>(null);

    const handleSubmit = async (formData: ConfigRequest) => {
        setLoading(true);
        setResult(null);
        try {
            const res = await axios.post('http://localhost:2137/genetic/submit', formData);
            setResult(res.data);
        } catch (err) {
            console.error('Request failed:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setResult(null);
    };

    return (
        <Box mx="auto" mt={4}>
            {!loading && !result && (
                <Box maxWidth="600px" mx="auto">
                    <Form onSubmit={handleSubmit} />
                </Box>
            )}

            {loading && (
                <Box textAlign="center" mt={4}>
                    <CircularProgress size={48} />
                    <Typography variant="body1" mt={2}>
                        Obliczanie...
                    </Typography>
                </Box>
            )}

            {result && !loading && <Result result={result} onReset={handleReset} />}
        </Box>
    );
}
