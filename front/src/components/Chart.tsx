import { Box, Typography } from '@mui/material';
import {
    Chart as ChartJS,
    LinearScale,
    PointElement,
    Tooltip,
    Legend,
    ChartOptions,
    ScatterController
} from 'chart.js';


ChartJS.register(LinearScale, PointElement, Tooltip, Legend, ScatterController);

import { Scatter } from 'react-chartjs-2';

type ChartProps = {
    data: number[];
}

const Chart = ({ data }: ChartProps) => {
    const chartData = {
        datasets: [{
            label: 'Wartość funkcji',
            data: data.map((val, idx) => ({
                x: idx + 1,
                y : val
            })),
            pointRadius: 5,
            backgroundColor: '#ff6361',
            hoverRadius: 5
        }]
    }

    const chartOptions: ChartOptions<'scatter'> = {
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                enabled: false,
            },
        },
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                min: 0,
                max: data.length + 1,
                title: {
                    display: true,
                    text: 'Epoka'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Wartość funkcji'
                }
            }
        }
    };


    return (
        <Box
            sx={{
                width: '80%',
                mx: 'auto',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                marginTop: 4,
                marginBottom: 10,
            }}
        >
            <Typography variant="h5" align="center" gutterBottom>
            Historia wartości funkcji w epokach dla najlepszego osobnika
            </Typography>
            <Scatter data={chartData} options={chartOptions} />
        </Box>
    )
}

export default Chart