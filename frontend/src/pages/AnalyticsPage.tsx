import AvgTimeChart from '../features/statistics/components/AvgTimeChart';
import TopUsersChart from '../features/statistics/components/TopUsersChart';

export default function AnalyticsPage() {
  return (
    <div>
      <h3 style={{}}>Длительность пребывание задач в статусах</h3>
      <section style={{}}>  
        <AvgTimeChart />
      </section>
      <section>
        <h3>Топ-3 продуктивных пользователей</h3>
        <TopUsersChart />
      </section>
    </div>
  );
}