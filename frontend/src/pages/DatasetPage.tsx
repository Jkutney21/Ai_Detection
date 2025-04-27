import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DisplayCard from "../components/DisplayCard";
import "./DatasetPage.css";

const DatasetPage: React.FC = () => {
  const { dataset } = useParams<{ dataset: string }>();
  const [classificationReport, setClassificationReport] = useState<string>("");
  const [topSpamEmails, setTopSpamEmails] = useState<string>("");

  const datasets: Record<string, { src: string; title: string }[]> = {
    easy_ham: [
      { src: "/plots/easy_ham/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/easy_ham/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/easy_ham/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
    easy_ham_2: [
      { src: "/plots/easy_ham_2/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/easy_ham_2/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/easy_ham_2/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
    hard_ham: [
      { src: "/plots/hard_ham/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/hard_ham/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/hard_ham/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
    spam: [
      { src: "/plots/spam/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/spam/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/spam/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
    spam_2: [
      { src: "/plots/spam_2/confusion_matrix.png", title: "Confusion Matrix" },
      { src: "/plots/spam_2/spam_vs_timestamp.png", title: "Spam vs Timestamp" },
      { src: "/plots/spam_2/top_tfidf_features.png", title: "Top TF-IDF Features" },
    ],
  };

  const images = datasets[dataset || ""] || [];

  useEffect(() => {
    if (dataset) {
      fetch(`/plots/${dataset}_results.txt`)
        .then((response) => {
          if (!response.ok) throw new Error("Result file not found.");
          return response.text();
        })
        .then((text) => {
          // Split the text into classification part and top emails part
          const parts = text.split("Top Spam-safe Emails:");
          if (parts.length === 2) {
            setClassificationReport(parts[0].trim());
            setTopSpamEmails(parts[1].trim());
          } else {
            setClassificationReport(text.trim());
            setTopSpamEmails("");
          }
        })
        .catch(() => {
          setClassificationReport("No results available for this dataset.");
          setTopSpamEmails("");
        });
    }
  }, [dataset]);

  return (
    <main role="main">
      <section className="jumbotron text-center" style={{ marginTop: 0 }}>
        <div className="j-container">
          <h1 className="jumbotron-heading">{dataset?.replace("_", " ").toUpperCase()} Plots</h1>
          <p className="text-muted" style={{ color: "white" }}>
            Visualizations for the {dataset?.replace("_", " ")} dataset.
          </p>
        </div>
      </section>

      <div className="album">
        <div className="container">
          <div className="row">
            {images.map((image, index) => (
              <div className="col" key={index}>
                <DisplayCard src={image.src} title={image.title} />
              </div>
            ))}
            {images.length === 0 && (
              <div className="col-12 text-center">
                <p>No plots found for this dataset.</p>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="row justify-content-center ">
            {/* Top Spam-safe Emails */}
            <div className="col-md-5 text-center">
              <h3 className="text-white">Top Spam-safe Emails</h3>
              <pre
                className="text-white rounded"
                style={{
                  backgroundColor: "transparent",
                  color: "white",
                  display: "inline-block",
                  whiteSpace: "pre-wrap",
                  textAlign: "left",
                  fontFamily: "Courier, monospace",
                  fontSize: "0.9rem",
                }}
              >
                {topSpamEmails || "No spam-safe emails available."}
              </pre>
            </div>

            {/* Classification Report */}
            <div className="col-md-5 text-center">
              <h3 className="text-white ">Classification Report</h3>
              <pre
                className="p-4 text-white rounded"
                style={{
                  backgroundColor: "transparent",
                  color: "white",
                  display: "inline-block",
                  whiteSpace: "pre-wrap",
                  textAlign: "left",
                  fontFamily: "Courier, monospace",
                  fontSize: "0.7rem",
                }}
              >
                {classificationReport}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default DatasetPage;