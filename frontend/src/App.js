import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import LandingPage from './pages/LandingPage';
import VideoFeedPage from './pages/VideoFeed';
import SmartSearch from './pages/SmartSearch';
import Anomalies from './pages/Anomalies';
import EmployeeInsights from './pages/EmployeeInsights';
import CustomCursor from './components/CustomCursor';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Cursor is global, but LandingPage also had it. 
            We can keep it here to be global, or let pages handle it. 
            Since Sidebar has hover effects, global is better. */}
        <CustomCursor />

        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard/video-feed" element={<VideoFeedPage />} />
          <Route path="/dashboard/smart-search" element={<SmartSearch />} />
          <Route path="/dashboard/anomalies" element={<Anomalies />} />
          <Route path="/dashboard/employee-insights" element={<EmployeeInsights />} />


          {/* Fallback for demo purposes */}
          <Route path="/dashboard/*" element={<VideoFeedPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
