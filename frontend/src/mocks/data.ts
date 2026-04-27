export const users = [
    { user_id: 1, login: 'alice', password: 'password', email: 'alice@example.com' },
    { user_id: 2, login: 'bob',   password: 'password', email: 'bob@example.com' },
    { user_id: 3, login: 'charlie', password: 'password', email: 'charlie@example.com' },
  ];
  
  export const tasks = [
    {
      task_id: 1,
      task_title: 'Создать макет главной страницы',
      description: 'Разработать дизайн и сверстать главную страницу',
      author_id: 1,
      current_status: 'В работе',
      assignee_id: 2,
    },
    {
      task_id: 2,
      task_title: 'Написать документацию API',
      description: 'Документировать все эндпоинты в Swagger',
      author_id: 1,
      current_status: 'Создана',
      assignee_id: 3,
    },
    {
      task_id: 3,
      task_title: 'Настроить CI/CD',
      description: 'Написать пайплайн для автоматического деплоя',
      author_id: 2,
      current_status: 'Выполнена',
      assignee_id: 1,
    },
    {
      task_id: 4,
      task_title: 'Пофиксить баг с авторизацией',
      description: 'При повторном логине не обновляется токен',
      author_id: 3,
      current_status: 'Создана',
      assignee_id: 1,
    },
    {
      task_id: 5,
      task_title: 'Рефакторинг модуля задач',
      description: 'Улучшить структуру кода в соответствии с паттернами',
      author_id: 2,
      current_status: 'В работе',
      assignee_id: 3,
    },
  ];