import React, { useState } from "react";

interface DisplayCardProps {
  src: string;
  title: string;
}

const DisplayCard: React.FC<DisplayCardProps> = ({ src, title }) => {
  const [isDetailedView, setIsDetailedView] = useState(false);

  return (
    <>
      {!isDetailedView ? (
        <div className="card mb-4 box-shadow" onClick={() => setIsDetailedView(true)} style={{ cursor: "pointer" }}>
          <img
            className="card-img-top"
            src={src}
            alt={title}
            style={{ height: "225px", width: "100%", objectFit: "cover" }}
          />
          <div className="card-body">
            <h5 className="card-title text-center">{title}</h5>
          </div>
        </div>
      ) : (
        <div
          className="modal fade show d-block"
          tabIndex={-1}
          role="dialog"
          style={{ backgroundColor: "rgba(0, 0, 0, 0.8)", position: "fixed", top: 0, left: 0, width: "100%", height: "100%" }}
          onClick={() => setIsDetailedView(false)} // Close detailed view on click
        >
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content bg-transparent border-0">
              <div className="modal-body text-center">
                <img
                  src={src}
                  alt={title}
                  className="img-fluid"
                  style={{ maxHeight: "90vh", maxWidth: "90vw" }}
                />
                <h5 className="text-white mt-3">{title}</h5>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DisplayCard;