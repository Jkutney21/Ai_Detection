import React, { useEffect } from "react";
import "./Theme.css"; // Import the CSS file for styling

const Theme: React.FC = () => {
  useEffect(() => {
    const container = document.getElementById("falling-container");
    if (container) {
      const createFallingImage = () => {
        const img = document.createElement("img");
        img.src = "/theme.png"; // Path to the image
        img.className = "falling-image";
        img.style.left = `${Math.random() * 100}vw`; // Random horizontal position
        img.style.animationDuration = `${3 + Math.random() * 5}s`; // Random fall duration
        img.style.opacity = `${0.5 + Math.random() * 0.5}`; // Random opacity
        container.appendChild(img);

        // Remove the image after the animation ends
        img.addEventListener("animationend", () => {
          container.removeChild(img);
        });
      };

      // Generate a random number of falling images
      const interval = setInterval(() => {
        createFallingImage();
      }, 500); // Create a new image every 500ms

      return () => clearInterval(interval); // Cleanup on component unmount
    }
  }, []);

  return <div id="falling-container" className="falling-container"></div>;
};

export default Theme;