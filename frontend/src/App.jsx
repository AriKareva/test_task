import React, { useState, useEffect } from 'react';

function App() {
  const [tasks, setTasks] = useState([]);
  const [text, setText] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch(`http://localhost:8000/tasks?search=${search}`)
      .then(res => res.json())
      .then(data => setTasks(data));
  }, [search]); 

  const addTask = async () => {
    await fetch('http://localhost:8000/tasks', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ title: text, user_id: 1 })
    });
    setText("");
    const res = await fetch('http://localhost:8000/tasks');
    const data = await res.json();
    setTasks(data);
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif' }}>
      <h1>Task Manager</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <input 
          placeholder="Search tasks..." 
          onChange={(e) => setSearch(e.target.value)} 
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <input 
          value={text} 
          onChange={(e) => setText(e.target.value)} 
          placeholder="New task title"
        />
        <button onClick={addTask}>Add Task</button>
      </div>

      <ul>
        {tasks.map(t => (
          <li key={Math.random()}>
            <strong>{t.title}</strong> — <small>Author: {t.user_name}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;