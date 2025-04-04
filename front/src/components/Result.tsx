import { Card, CardContent, Typography, Button, Box } from '@mui/material';
import { GenericAlgorithmResponse } from '../models/generic-algorithm-response.model';
import Chart from './Chart';

type ResultProps = {
    result: GenericAlgorithmResponse;
    onReset: () => void;
};

const Result = ({ result, onReset }: ResultProps) => {
    const roundNumber = (num: number, precision: number) => Math.round(num * Math.pow(10, precision)) / Math.pow(10, precision);

    return (
        <>
            <Box maxWidth={'600px'} mx="auto" mt={4}>
                <Card>
                    <CardContent>
                        <Typography variant="h6">Wynik:</Typography>
                        <Typography variant="body1">
                            <b>Najlepszy gen końcowy:</b> {result.genes}
                        </Typography>
                        <Typography variant="body1">
                            <b>Współrzędne punktu minimum:</b> ({result.points.map(item => roundNumber(item, 4)).join(', ')})
                        </Typography>
                        <Typography variant="body1">
                            <b>Znalezione minimum globalne:</b> {roundNumber(+result.fitness, 4)}
                        </Typography>
                        <Typography variant="body1">
                            <b>Czas trwania:</b> {result.elapsed_time} s
                        </Typography>
                        <Button variant="outlined" onClick={onReset} style={{ marginTop: '1rem' }}>
                            Wykonaj ponownie
                        </Button>
                    </CardContent>
                </Card>
            </Box>
            <Box sx={{ width: '100%'}} >
                <Chart data={result.history} />
            </Box>
        </>
    );
};

export default Result;
