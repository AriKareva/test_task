import { useQuery } from '@tanstack/react-query';
import { fetchStatusAvgTime } from '../../../api/statistics';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

interface AvgTimeData {
  status_title: string;
  days: number;
  hours: number;
  minutes: number;
  avg_duration_sec: number;
}

function toTotalMinutes(item: AvgTimeData): number {
  return item.avg_duration_sec / 60;
}

export default function AvgTimeChart() {
  const { data, isLoading, error } = useQuery<AvgTimeData[]>({
    queryKey: ['statusAvgTime'],
    queryFn: fetchStatusAvgTime,
  });

  if (isLoading) return <div className="loading">Загрузка...</div>;
  if (error || !data) return <div className="loading">Ошибка загрузки статистики</div>;

  const chartData = data.map(item => ({
    ...item,
    totalMinutes: toTotalMinutes(item),
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const record = payload[0].payload;
      return (
        <div style={{ background: '#fff', padding: 8, border: '1px solid #ccc', borderRadius: 4 }}>
          <p><strong>{record.status_title}</strong></p>
          <p>{`${record.days} д ${record.hours} ч ${record.minutes} мин`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ width: '100%', minWidth: '300px', height: 350 }}>
      <ResponsiveContainer>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="status_title"
            angle={-45}
            textAnchor="end"
            interval={0}
            height={70}
            tick={{ fontSize: 12 }}
          />
          <YAxis unit=" мин" />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar dataKey="totalMinutes" fill="#6366f1" name="Общее время (мин)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}