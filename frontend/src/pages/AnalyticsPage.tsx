import AvgTimeChart from '../features/statistics/components/AvgTimeChart';
import TopUsersChart from '../features/statistics/components/TopUsersChart';

export default function AnalyticsPage() {
  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>Аналитика</h2>
      <section style={{ marginBottom: 32 }}>
        <h3>Среднее время в статусах</h3>
        <AvgTimeChart />
      </section>
      <section>
        <h3>Топ‑3 продуктивных пользователей</h3>
        <TopUsersChart />
      </section>
    </div>
  );
}