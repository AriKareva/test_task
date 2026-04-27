// import { useQuery } from '@tanstack/react-query';
// import { fetchTopProductiveUsers } from '../../../api/statistics';
// import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

// export default function TopUsersChart() {
//   const { data, isLoading, error } = useQuery({
//     queryKey: ['topProductiveUsers'],
//     queryFn: () => fetchTopProductiveUsers(3),
//   });

//   if (isLoading) return <div className="loading">Загрузка...</div>;
//   if (error || !data) return <div className="loading">Ошибка загрузки топ-пользователей</div>;

//   const chartData = data.map((u: any) => ({
//     name: u.login,
//     'Среднее время до Done (мин)': u.avg_minutes,
//   }));

//   return (
//     <BarChart width={600} height={300} data={chartData} layout="vertical">
//       <CartesianGrid strokeDasharray="3 3" />
//       <XAxis type="number" />
//       <YAxis dataKey="name" type="category" />
//       <Tooltip />
//       <Legend />
//       <Bar dataKey="Среднее время до Done (мин)" fill="#82ca9d" />
//     </BarChart>
//   );
// }