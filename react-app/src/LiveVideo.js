import React, { useState, useEffect } from 'react';

const LiveVideo = () => {
  const [videoUrl, setVideoUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Define an async function to fetch the video URL
    async function fetchVideoUrl() {
      try {
        setLoading(true);
        const response = await fetch('http://127.0.0.1:5000/stream/0'); // Replace with your API endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch video");
        }
        const data = await response.json();
        setVideoUrl(data.url); // Assuming the API returns { "url": "video-url.mp4" }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchVideoUrl();
  }, []);

  if (loading) return <div>Loading video...</div>;
  if (error) return <div>Error loading video: {error}</div>;

  return (
    <div>
      {videoUrl ? (
        <video src={videoUrl} controls autoPlay style={{ width: '100%', height: 'auto' }} />
      ) : (
        <div>Video not available</div>
      )}
    </div>
  );
};

export default LiveVideo;