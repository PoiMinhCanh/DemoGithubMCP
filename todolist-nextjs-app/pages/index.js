
import { useState } from 'react';
import styles from '../styles/TodoList.module.css';

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
    <div className={styles.container}>
      <h1 className={styles.title}>Todo List</h1>
      <form onSubmit={addTodo} className={styles.form}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Add a new todo"
          className={styles.input}
        />
        <button type="submit" className={styles.addBtn}>Add</button>
      </form>
      <ul className={styles.list}>
        {todos.map((todo, idx) => (
          <li key={idx} className={styles.listItem}>
            <span>{todo}</span>
            <button onClick={() => removeTodo(idx)} className={styles.removeBtn}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
