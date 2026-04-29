echo "Останавливаем контейнеры и удаляем том с данными..."
docker compose down -v

echo "Запускаем контейнеры заново (MySQL выполнит init.sql)..."
docker compose up -d

echo "Ждём, пока MySQL станет доступен..."
until docker exec -i test_mysql mysqladmin ping -h localhost --silent; do
    sleep 2
done

echo "База данных пересоздана и заполнена тестовыми данными."