import React, { useState, useRef, useEffect, useCallback } from "react";
import { Button } from "react-bootstrap";
import "./ScreenshotComponent.css";
import axios from 'axios';

const ScreenshotComponent = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [isSelecting, setIsSelecting] = useState(false);
  const [startPos, setStartPos] = useState({ x: 0, y: 0 });
  const [currentPos, setCurrentPos] = useState({ x: 0, y: 0 });
  const overlayRef = useRef<HTMLDivElement | null>(null);

  // Memoize event handlers to prevent stale closures
  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (!isDragging || !isSelecting) return;
      e.preventDefault();
      setCurrentPos({ x: e.clientX, y: e.clientY });
    },
    [isDragging, isSelecting]
  );

  const handleMouseUp = useCallback(() => {
    if (!isDragging || !isSelecting) return;
    
    // Calculate final coordinates
    const left = Math.min(startPos.x, currentPos.x);
    const top = Math.min(startPos.y, currentPos.y);
    const width = Math.abs(startPos.x - currentPos.x);
    const height = Math.abs(startPos.y - currentPos.y);

    setIsDragging(false);
    setIsSelecting(false);
    const boundingBox = {
      top: top,
      left: left,
      width: width,
      height: height,
    };

    if (width > 0 && height > 0) {
      axios.post('http://localhost:5000/size', boundingBox)
        .then(response => {
            console.log('Bounding box saved:', response.data);
        })
        .catch(error => {
            console.error('Error saving bounding box:', error);
        });
    }
  }, [isDragging, isSelecting, startPos, currentPos]);

  const startSelection = () => {
    setIsDragging(true);
    setIsSelecting(false);
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsSelecting(true);
    setStartPos({ x: e.clientX, y: e.clientY });
    setCurrentPos({ x: e.clientX, y: e.clientY });
  };

  useEffect(() => {
    if (isDragging) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    }

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isDragging, handleMouseMove, handleMouseUp]);

  return (
    <div className="screenshot-container">
      {isDragging && (
        <div
          ref={overlayRef}
          className="selection-overlay"
          onMouseDown={handleMouseDown}
        >
          {isSelecting && (
            <div
              className="selection-box"
              style={{
                left: Math.min(startPos.x, currentPos.x),
                top: Math.min(startPos.y, currentPos.y),
                width: Math.abs(currentPos.x - startPos.x),
                height: Math.abs(currentPos.y - startPos.y),
              }}
            />
          )}
        </div>
      )}

      <div className="main-content" style={{ pointerEvents: isDragging ? "none" : "auto" }}>
        <Button
          onClick={startSelection}
          variant="primary"
          className="screenshot-button"
        >Screen Selection
        </Button>
      </div>
    </div>
  );
};

export default ScreenshotComponent;