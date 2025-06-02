import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [form, setForm] = useState({
    name: '',
    phone: '',
    hour: '',
    minute: '',
    tone: 'gentle',
  });
  const [status, setStatus] = useState('');

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const submitForm = async () => {
    try {
      const response = await axios.post('http://localhost:8000/schedule', form);
      setStatus(response.data.status);
    } catch (err) {
      setStatus('Failed to schedule.');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Wake-Up Call Assistant</h2>
      <input name="name" placeholder="Your name" onChange={handleChange} /><br />
      <input name="phone" placeholder="+15551234567" onChange={handleChange} /><br />
      <input name="hour" type="number" placeholder="Hour (0-23)" onChange={handleChange} /><br />
      <input name="minute" type="number" placeholder="Minute (0-59)" onChange={handleChange} /><br />
      <select name="tone" onChange={handleChange}>
        <option value="gentle">Gentle</option>
        <option value="tough love">Tough Love</option>
        <option value="spiritual">Spiritual</option>
      </select><br /><br />
      <button onClick={submitForm}>Schedule Call</button>
      <p>{status}</p>
    </div>
  );
}

export default App;
