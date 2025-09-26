import { useState } from 'react';

export default function Home() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setTodos([...todos, input]);
    setInput('');
  };

  const removeTodo = (idx) => {
    setTodos(todos.filter((_, i) => i !== idx));
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>Todo List</h1>
      <form onSubmit={addTodo} style={{ display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Add a new todo"
          style={{ flex: 1 }}
        />
        <button type="submit">Add</button>
      </form>
      <ul style={{ padding: 0, listStyle: 'none', marginTop: 20 }}>
        {todos.map((todo, idx) => (
          <li key={idx} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span>{todo}</span>
            <button onClick={() => removeTodo(idx)} style={{ color: 'red' }}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
