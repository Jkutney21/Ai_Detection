import React from "react";
import { useParams } from "react-router-dom";
import DisplayCard from "../components/DisplayCard";

const DatasetPage: React.FC = () => {
  const { dataset } = useParams<{ dataset: string }>();

  const datasets: Record<string, { src: string; title: string }[]> = {
    easy_ham: [
      { src: "/plots/easy_ham/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/easy_ham/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/easy_ham/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
    easy_ham_2: [
      { src: "/plots/easy_ham/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/easy_ham/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/easy_ham/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
    hard_ham: [
      { src: "/plots/easy_ham/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/easy_ham/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/easy_ham/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
    spam: [
      { src: "/plots/easy_ham/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/easy_ham/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/easy_ham/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
    spam_2: [
      { src: "/plots/easy_ham/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/easy_ham/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/easy_ham/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
  };

  const images = datasets[dataset || ""] || [];

  return (
    <main role="main">
      <section className="jumbotron text-center">
        <div className="container">
          <h1 className="jumbotron-heading">{dataset?.replace("_", " ").toUpperCase()} Plots</h1>
          <p className="lead text-muted">
            Visualizations for the {dataset?.replace("_", " ")} dataset.
          </p>
        </div>
      </section>

      <div className="album py-5 bg-light">
        <div className="container">
          <div className="row">
            {images.map((image, index) => (
              <div className="col-md-4" key={index}>
                <DisplayCard src={image.src} title={image.title} />
              </div>
            ))}
            {images.length === 0 && (
              <div className="col-12 text-center">
                <p>No plots found for this dataset.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
};

export default DatasetPage;