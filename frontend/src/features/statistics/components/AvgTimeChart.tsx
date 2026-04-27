// import { useQuery } from '@tanstack/react-query';
// import { fetchStatusAvgTime } from '../../../api/statistics';
// import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

// export default function AvgTimeChart() {
//   const { data, isLoading, error } = useQuery({
//     queryKey: ['statusAvgTime'],
//     queryFn: fetchStatusAvgTime,
//   });

//   if (isLoading) return <div className="loading">Загрузка...</div>;
//   if (error || !data) return <div className="loading">Ошибка загрузки статистики</div>;

//   return (
//     <BarChart width={600} height={300} data={data}>
//       <CartesianGrid strokeDasharray="3 3" />
//       <XAxis dataKey="status_title" />
//       <YAxis unit=" мин" />
//       <Tooltip />
//       <Legend />
//       <Bar dataKey="avg_minutes" fill="#6366f1" name="Среднее время (мин)" />
//     </BarChart>
//   );
// }