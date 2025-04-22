import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import { createRoot } from 'react-dom/client';
import './index.css';
import Background from './background';
import Search from './Search';
import ErrorBoundary from './ErrorBoundary';
import ScreenshotComponent from './ScreenshotComponent';



function Main() {

  
  const socketRef = useRef<WebSocket | null>(null);
  const [captureRunning, setCaptureRunning] = useState(false);
  

  // Toggle screen capture
  const toggleCapture = async () => {
    try {
      const response = await axios.post('http://localhost:5000/capture');
      console.log(response.data);
      setCaptureRunning(response.data.status === 'true');
    } catch (error) {
      console.error('Error toggling capture:', error);
    }
  };
  useEffect(() => {
    if (captureRunning) {
      // Delay WebSocket connection by 4 seconds (4000ms)
      const timer = setTimeout(() => {
        const socket = new WebSocket('ws://localhost:5001');
        socketRef.current = socket;
  
        socket.onmessage = (event) => {
          const image = document.getElementById('screen') as HTMLImageElement;
          if (image) {
            image.src = 'data:image/png;base64,' + event.data;
            image.style.display = 'block';
          }
        };
  
        socket.onopen = () => {
          console.log('WebSocket connection established');
        };
  
        socket.onclose = () => {
          console.log('WebSocket connection closed');
        };
  
        socket.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
  
        // Cleanup function to close WebSocket connection
        return () => {
          if (socketRef.current) {
            socketRef.current.close();
            socketRef.current = null;
          }
        };
      }, 4000); // 4000ms = 4 seconds delay
  
      // Cleanup the timeout if the component unmounts or captureRunning changes
      return () => {
        clearTimeout(timer);
      };
    }
  }, [captureRunning]); // Re-run effect when captureRunning changes

  return (
    <div className='main'>
      <div className="button-container">
        <button onClick={toggleCapture}>
          {captureRunning ? 'End Capture' : 'Start Capture'}
        </button>
      </div>
      
      <img 
  id="screen" 
  src="" 
  alt="Screen Capture" 
  style={{
    display: captureRunning ? 'block' : 'none',
    position: 'fixed',
    top: '60%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    transition: 'all 0.3s ease',
    cursor: 'pointer',
    borderRadius: '15px',
    
  }} 
/>
      
      <ErrorBoundary>
      {captureRunning ? null : <ScreenshotComponent />}
      <Search />
      </ErrorBoundary>
      <Background/>
    </div>
  );
}

const rootElement = document.getElementById('root');
if (rootElement) {
  const root = createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <Main />
    </React.StrictMode>
  );
}