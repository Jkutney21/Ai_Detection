import React from "react";
import './home.css';

const Home: React.FC = () => {
  const backgroundStyle: React.CSSProperties = {
    backgroundImage: "url('/home.png')",
    backgroundSize: "contain", // Adjust to fit the entire image without cropping
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",
    height: "100vh", 
    display: "flex", // Flexbox for centering
    flexDirection: "column", // Stack elements vertically
    justifyContent: "center", // Center vertically
    alignItems: "center", // Center horizontally
    color: "white",
    overflow: "hidden", // Prevent scrolling
  };

  return (
    
    <div id="home-background" style={backgroundStyle}>
      <h1 id="home-title" className="display-4">Welcome to Spam Detection</h1>
      <p id="home-description" className="display-4 text-center ">
        Detect spam emails with ease using our advanced AI tools.
      </p>
    </div>
  );
};

export default Home;