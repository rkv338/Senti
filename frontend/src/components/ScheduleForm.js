import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { fromZonedTime, toZonedTime, formatInTimeZone } from 'date-fns-tz';
import './ScheduleForm.css';

const ScheduleForm = () => {
  const [form, setForm] = useState({
    name: '',
    phone: '',
    timestamp: '',
    tone: 'gentle',
  });
  const [status, setStatus] = useState('');
  const [userTimeZone, setUserTimeZone] = useState('');
  const [cstDateTime, setCstDateTime] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [actionType, setActionType] = useState(''); // 'schedule' or 'call-now'

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleDateTimeChange = (e) => {
    const input = e.target.value;
    setForm({ ...form, timestamp: input });
    
    if (!input) {
      setCstDateTime('');
      return;
    }

    try {
      // Convert local time input to UTC using user's timezone
      const utcDate = fromZonedTime(input, userTimeZone);
      console.log(utcDate);
      // Convert UTC to CST
      const cstDate = toZonedTime(utcDate, 'America/Chicago');

      // Format the CST datetime
      const formattedCST = formatInTimeZone(cstDate, 'America/Chicago', "yyyy-MM-dd'T'HH:mm:ssXXX");

      setCstDateTime(formattedCST);
    } catch (error) {
      console.error('Error converting timezone:', error);
      setCstDateTime('Error converting timezone');
    }
  };

  const submitForm = async () => {
    if (!form.name || !form.phone || !form.timestamp) {
      setStatus('Please fill in all required fields.');
      return;
    }

    setIsLoading(true);
    setActionType('schedule');
    try {
      // Create payload with CST timestamp
      const payload = {
        ...form,
      };
      
      console.log('Sending payload:', payload);
      console.log('Making request to: http://localhost:8000/schedule');
      
      const response = await axios.post('http://localhost:8000/schedule', payload);
      console.log('Response received:', response);
      setStatus('Your call has been scheduled successfully!');
    } catch (err) {
      console.error('Request failed:', err);
      console.error('Error details:', err.response?.data || err.message);
      setStatus(`Failed to schedule: ${err.response?.data?.message || err.message || 'Please try again.'}`);
    } finally {
      setIsLoading(false);
      setActionType('');
    }
  };

  const callNow = async () => {
    if (!form.name || !form.phone) {
      setStatus('Please fill in your name and phone number for immediate call.');
      return;
    }

    setIsLoading(true);
    setActionType('call-now');
    try {
      const payload = {
        name: form.name,
        phone: form.phone,
        tone: form.tone
      };
      
      console.log('Sending call now payload:', payload);
      console.log('Making request to: http://localhost:8000/call-now');
      
      const response = await axios.post('http://localhost:8000/call-now', payload);
      console.log('Response received:', response);
      setStatus('Your call has been initiated! You should receive a call shortly.');
    } catch (err) {
      console.error('Request failed:', err);
      console.error('Error details:', err.response?.data || err.message);
      setStatus(`Failed to initiate call: ${err.response?.data?.message || err.message || 'Please try again.'}`);
    } finally {
      setIsLoading(false);
      setActionType('');
    }
  };
  
  const getUserTimeZone = () => {
    const {timeZone} = Intl.DateTimeFormat().resolvedOptions();
    return timeZone;
  }
  
  useEffect(() => {
    setUserTimeZone(getUserTimeZone());
  }, []);

  const toneDescriptions = {
    gentle: "A warm, encouraging wake-up with positive affirmations",
    "tough love": "Direct, motivational approach to help you start strong",
    spiritual: "Mindful, peaceful awakening with calming presence"
  };

  return (
    <div className="schedule-form">
      <div className="form-group">
        <label htmlFor="name" className="form-label">
          Your Name
          <span className="required">*</span>
        </label>
        <input 
          id="name"
          name="name" 
          placeholder="Enter your first name" 
          onChange={handleChange}
          value={form.name}
          className="form-input"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="phone" className="form-label">
          Phone Number
          <span className="required">*</span>
        </label>
        <input 
          id="phone"
          name="phone" 
          placeholder="+1 (555) 123-4567" 
          onChange={handleChange}
          value={form.phone}
          className="form-input"
          type="tel"
          required
        />
        <span className="form-hint">Include country code (e.g., +1 for US)</span>
      </div>

      <div className="form-group">
        <label htmlFor="timestamp" className="form-label">
          Preferred Wake-up Time
          <span className="required">*</span>
        </label>
        <input 
          id="timestamp"
          name="timestamp" 
          type="datetime-local" 
          onChange={handleDateTimeChange}
          value={form.timestamp}
          className="form-input"
          required
        />
        <span className="form-hint">
          Your timezone: <strong>{userTimeZone}</strong>
        </span>
      </div>

      <div className="form-group">
        <label htmlFor="tone" className="form-label">
          Call Tone
        </label>
        <div className="tone-selection">
          {Object.entries(toneDescriptions).map(([value, description]) => (
            <label key={value} className={`tone-option ${form.tone === value ? 'selected' : ''}`}>
              <input
                type="radio"
                name="tone"
                value={value}
                checked={form.tone === value}
                onChange={handleChange}
                className="tone-radio"
              />
              <div className="tone-content">
                <span className="tone-name">
                  {value.charAt(0).toUpperCase() + value.slice(1)}
                </span>
                <span className="tone-description">{description}</span>
              </div>
            </label>
          ))}
        </div>
      </div>
      
      <div className="button-group">
        <button 
          onClick={callNow}
          disabled={isLoading}
          className={`call-now-button ${isLoading && actionType === 'call-now' ? 'loading' : ''}`}
        >
          {isLoading && actionType === 'call-now' ? (
            <>
              <span className="loading-spinner"></span>
              Connecting...
            </>
          ) : (
            <>
              📞 Call Now
            </>
          )}
        </button>
        
        <button 
          onClick={submitForm}
          disabled={isLoading}
          className={`submit-button ${isLoading && actionType === 'schedule' ? 'loading' : ''}`}
        >
          {isLoading && actionType === 'schedule' ? (
            <>
              <span className="loading-spinner"></span>
              Scheduling...
            </>
          ) : (
            'Schedule My Wellness Wake-Up Call'
          )}
        </button>
      </div>
      
      {status && (
        <div className={`status-message ${status.includes('Failed') || status.includes('Please fill') ? 'error' : 'success'}`}>
          <div className="status-icon">
            {status.includes('Failed') || status.includes('Please fill') ? '⚠️' : '✅'}
          </div>
          <span>{status}</span>
        </div>
      )}
    </div>
  );
};

export default ScheduleForm; 