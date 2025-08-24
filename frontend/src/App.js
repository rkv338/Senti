import React from 'react';
import ScheduleForm from './components/ScheduleForm';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Senti</h1>
          <p className="hero-subtitle">Your personal mental health companion</p>
          <p className="hero-description">
            Start each day with intention. Schedule a gentle wake-up call that supports your mental wellness journey.
          </p>
        </div>
      </div>
      
      <div className="main-content">
        <div className="form-container">
          <h2 className="form-title">Schedule Your Wellness Call</h2>
          <p className="form-description">
            Choose your preferred tone and time for a personalized wake-up experience designed to promote positive mental health.
          </p>
          <ScheduleForm />
        </div>
      </div>
      
      <footer className="footer">
        <p>Taking care of your mental health, one day at a time.</p>
      </footer>
    </div>
  );
}

export default App;
