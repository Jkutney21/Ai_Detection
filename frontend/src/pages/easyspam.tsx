import React, { useState } from "react";

const EasySpam: React.FC = () => {
  const images = [
    {
      src: "/plots/easy_ham/confusion_matrix.png",
      title: "Confusion Matrix",
    },
    {
      src: "/plots/easy_ham/spam_vs_timestamp.png",
      title: "Spam vs Timestamp",
    },
    {
      src: "/plots/easy_ham/top_tfidf_features.png",
      title: "Top TF-IDF Features",
    },
  ];

  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  return (
    <main role="main">
      <section className="jumbotron text-center">
        <div className="container">
          <h1 className="jumbotron-heading">Easy Ham Plots</h1>
          <p className="lead text-muted">
            Visualizations for the Easy Ham dataset.
          </p>
        </div>
      </section>

      <div className="album py-5 bg-light">
        <div className="container">
          <div className="row">
            {images.map((image, index) => (
              <div className="col-md-4" key={index}>
                <div className="card mb-4 box-shadow">
                  <img
                    className="card-img-top"
                    src={image.src}
                    alt={image.title}
                    style={{ height: "225px", width: "100%", objectFit: "cover", cursor: "pointer" }}
                    onClick={() => setSelectedImage(image.src)}
                  />
                  <div className="card-body">
                    <h5 className="card-title text-center">{image.title}</h5>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {selectedImage && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0,0,0,0.8)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
          onClick={() => setSelectedImage(null)}
        >
          <img
            src={selectedImage}
            alt="Full Size"
            style={{ maxHeight: "90%", maxWidth: "90%", borderRadius: "10px" }}
          />
        </div>
      )}
    </main>
  );
};

export default EasySpam;
