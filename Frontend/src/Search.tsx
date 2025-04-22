import React, { useState, useEffect } from 'react';
import './Search.css';
import axios from 'axios';

interface GoogleResult {
  content: string;
}

const Search: React.FC = () => {
  const [results, setResults] = useState<GoogleResult[]>([]);
  const [googleError, setGoogleError] = useState<string>('');
  const [logs, setLogs] = useState<string>(''); // State for logs

  // Fetch Google data
  const fetchGoogleData = async () => {
    try {
      const response = await axios.get<{ status: string; google: string }>('http://localhost:5000/google');
      
      if (response.data.status === "Success") {
        const lines = response.data.google.split('\n')
          .filter(line => line.trim() !== '')
          .map(line => ({ content: line }));

        setResults(lines);
        setGoogleError('');
      } else {
        throw new Error('Server returned error status for Google');
      }
    } catch (error) {
      console.error('Error fetching Google data:', error);
      setGoogleError('Failed to load Google results');
      setResults([]);
    }
  };

  // Fetch logs
  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://localhost:5000/Logs');
      console.log(response.data); // Log the response to confirm
      setLogs(response.data.logs);
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  };

  useEffect(() => {
    // Initial fetch
    const fetchAllData = async () => {
      await fetchGoogleData();
      await fetchLogs();
    };
    fetchAllData();

    // Poll for new data every 10 seconds
    const interval = setInterval(() => {
      fetchGoogleData();
      fetchLogs();
    }, 10000);

    // Cleanup interval on unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <div className="googlebox">
        <div className="google">Search:</div>
        {googleError && <div className="error-message">{googleError}</div>}
        {!googleError && results.map((item, index) => (
          <div key={`${index}-${item.content}`} className="google-item">
            <div className="result-content">
              {item.content.split('. ').map((part, i) => (
                <p style={{ marginTop: '10px' }} key={i}>{part}</p>
              ))}
            </div>
          </div>
        ))}
      </div>
      <div className="box box2">
        <h2 className='right'>Logs:</h2>
        <p style={{ marginTop: '5px' }}>{logs}</p>
      </div>
    </div>
  );
};

export default Search;