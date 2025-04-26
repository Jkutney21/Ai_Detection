import React from "react";

const Header: React.FC = () => {
  return (
    <header className="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
      <a
        href="/"
        className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none"
      >
        <svg className="bi me-2" width="40" height="32">
          <use xlinkHref="#bootstrap"></use>
        </svg>
        <span className="fs-4">Spam Detection</span>
      </a>

      <ul className="nav nav-pills">
        <li className="nav-item">
          <a href="/easy_ham" className="nav-link">
            Easy Ham
          </a>
        </li>
        <li className="nav-item">
          <a href="/easy_ham_2" className="nav-link">
            Easy Ham 2
          </a>
        </li>
        <li className="nav-item">
          <a href="/hard_ham" className="nav-link">
            Hard Ham
          </a>
        </li>
        <li className="nav-item">
          <a href="/spam" className="nav-link">
            Spam
          </a>
        </li>
        <li className="nav-item">
          <a href="/spam_2" className="nav-link">
            Spam 2
          </a>
        </li>
      </ul>
    </header>
  );
};

export default Header;
