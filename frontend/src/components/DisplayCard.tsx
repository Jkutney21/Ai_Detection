import React, { useState } from "react";
import "./DisplayCard.css"; // Import the CSS file for styling

interface DisplayCardProps {
  src: string;
  title: string;
}

const DisplayCard: React.FC<DisplayCardProps> = ({ src, title }) => {
  const [isDetailedView, setIsDetailedView] = useState(false);

  return (
    <>
      {!isDetailedView ? (
        <div
          className="card mb-3 box-shadow"
          onClick={() => setIsDetailedView(true)}
          style={{
            cursor: "pointer",
            width: "200px", // Smaller card width
            margin: "0 auto", // Center the card and add spacing
          }}
        >
          <img
            className="card-img-top"
            src={src}
            alt={title}
            style={{
              height: "150px", // Smaller image height
              width: "100%",
              objectFit: "cover",
            }}
          />
          <div className="card-body">
            <h6 className="card-title text-center" style={{ fontSize: "1rem" }}>
              {title}
            </h6>
          </div>
        </div>
      ) : (
        <div
          className="modal fade show d-block"
          tabIndex={-1}
          role="dialog"
          style={{
            backgroundColor: "rgba(0, 0, 0, 0.8)",
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
          }}
          onClick={() => setIsDetailedView(false)} // Close detailed view on click
        >
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content confusion-matrix">
             
                <img
                  src={src}
                  alt={title}
                  className="img-fluid"
                  style={{
                    maxHeight: "220vh", // Increased modal image height
                    maxWidth: "320vw", // Increased modal image width
                  }}
                />
                
            
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DisplayCard;