// App.js
import React, { useEffect, useRef } from 'react';
import './App.css';

function App() {
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current) {
      // Set the video source to the live stream
      videoRef.current.src = 'http://127.0.0.1:5000/stream/0';
    }
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Security Dashboard</h1>
      </header>
      <main className="app-content">
        <div className="video-container">
          <h2>Live Video Feed</h2>
          <video
            ref={videoRef}
            controls
            autoPlay
            muted
            style={{
              width: '100%',
              border: '1px solid #ddd',
              borderRadius: '8px',
              boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.2)'
            }}
          />
        </div>
        {/* Additional UI components or information */}
      </main>
    </div>
  );
}

export default App;



// src/App.js
// import React from 'react';
// import LiveVideo from './LiveVideo';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <h1>Crime Catcher!</h1>
//       <LiveVideo />
//     </div>
//   );
// }

// export default App;
