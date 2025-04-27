import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/header";
import Footer from "./components/footer";
import DatasetPage from "./pages/DatasetPage";
import Home from "./pages/home";
import "./App.css"; // Assuming you have some global styles
import "bootstrap/dist/css/bootstrap.min.css"; // Bootstrap CSS
import Theme from "./components/Theme";

const App: React.FC = () => {
  return (
    <Router>
       <Theme/>
        <div className="main-layout d-flex">
        {/* Left Panel */}
        <aside className="left-panel ">
         
        </aside>
      <Header />
    

        {/* Main Content */}
        <main className="main-content flex-grow-1 p-3">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/:dataset" element={<DatasetPage />} />
          </Routes>
        </main>

       
      <Footer />
       {/* Right Panel */}
        <aside className="right-panel ">
          
        </aside>
      </div>
    </Router>
  );
};

export default App;