import { useQuery } from '@tanstack/react-query';
import { fetchTopProductiveUsers } from '../../../api/statistics';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

interface ProductiveUserData {
  login: string;
  days: number;
  hours: number;
  minutes: number;
  completion_time_sec: number;
}

function toTotalMinutes(item: ProductiveUserData): number {
  return item.completion_time_sec / 60;
}

export default function TopUsersChart() {
  const { data, isLoading, error } = useQuery<ProductiveUserData[]>({
    queryKey: ['topProductiveUsers'],
    queryFn: () => fetchTopProductiveUsers(),
  });

  if (isLoading) return <div className="loading">Загрузка...</div>;
  if (error || !data?.length) return <div className="loading">Нет данных</div>;

  const chartData = data.map(item => ({
    ...item,
    totalMinutes: toTotalMinutes(item),
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const record = payload[0].payload;
      return (
        <div style={{ background: '#fff', padding: 8, border: '1px solid #ccc', borderRadius: 4 }}>
          <p><strong>{record.login}</strong></p>
          <p>{`${record.days} д ${record.hours} ч ${record.minutes} мин`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={chartData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" unit=" мин" />
          <YAxis dataKey="login" type="category" />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar dataKey="totalMinutes" fill="#6366f1" name="Время до завершения задачи (мин)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}