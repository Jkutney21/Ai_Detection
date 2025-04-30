import React from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom
import "./header.css"; // Assuming you have some CSS for styling
import "bootstrap/dist/css/bootstrap.min.css"; // Bootstrap CSSS

const Header: React.FC = () => {
  return (
    <header className="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
      <Link
        to="/" // Use Link for navigation to the Home component
        className="d-flex align-items-center mb-3 mb-md-0 me-md-auto  text-decoration-none"
        style={{ marginLeft: "20px" ,color:"white"}} // Move the element to the left
      >
        <img
    src="/spam.png"
    alt="Spam Detection Logo"
    width="40"
    height="32"
    className="me-2"
  />
  <span className="fs-4">Spam Detection</span>
  <img
    src="/spam.png"
    alt="Spam Detection Logo"
    width="40"
    height="32"
    className="me-2"
    style={{ marginLeft: "10px" }}
  />
      </Link>

      <ul className="nav nav-pills">
      
        <li className="nav-item">
          <Link to="/easy_ham" className="nav-link">
            Easy Ham
          </Link>
        </li>
        <li className="nav-item">
          <Link to="/easy_ham_2" className="nav-link">
            Easy Ham 2
          </Link>
        </li>
        <li className="nav-item">
          <Link to="/hard_ham" className="nav-link">
            Hard Ham
          </Link>
        </li>
        <li className="nav-item">
          <Link to="/spam" className="nav-link">
            Spam
          </Link>
        </li>
        <li className="nav-item"
         style={{ marginRight: "20px" }} // Move the element to the left
        >
          <Link to="/spam_2" className="nav-link">
            Spam 2
          </Link>
        </li>
      </ul>
    </header>
  );
};

export default Header;