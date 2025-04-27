import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/header"; // Fixed import path
import DatasetPage from "./pages/DatasetPage";
import "./App.css"; // Assuming you have some global styles
import Footer from "./components/footer";
import "bootstrap/dist/css/bootstrap.min.css"; // Bootstrap CSS


const App: React.FC = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<h1 className="text-center mt-5">Welcome to Spam Detection!</h1>} />
        <Route path="/:dataset" element={<DatasetPage />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;