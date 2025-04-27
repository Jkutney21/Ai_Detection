import React from "react";
import './footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="d-flex justify-content-center align-items-center py-3 border-top">
      {/* Footer Logo */}
      <img
        src="/footer.png"
        alt="Footer Logo"
        width="50"
        height="50"
        className="img-fluid me-3"
      />

      {/* Footer Links */}
      <div className="d-flex align-items-center">
        <a
          href="https://github.com/Jkutney21/ML_Class_Project"
          target="_blank"
          rel="noopener noreferrer"
          className="text-decoration-none me-2"
        >
          Source Code
        </a>
        |
        <a
          href="https://spamassassin.apache.org/old/publiccorpus/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-decoration-none ms-2"
        >
          Dataset
        </a>
      </div>

      {/* Footer Logo */}
      <img
        src="/footer.png"
        alt="Footer Logo"
        width="50"
        height="50"
        className="img-fluid ms-3"
      />
    </footer>
  );
};

export default Footer;