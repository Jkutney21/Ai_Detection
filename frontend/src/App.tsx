
import "bootstrap/dist/css/bootstrap.min.css";
import Header from './components/header'
import './App.css'
import Footer from './components/footer'
import EasySpam from "./pages/easyspam";

function App() {
  

  return (
    <>
      <Header/>
      <main className="container">
        <EasySpam/>
       </main>
      <Footer/>
    </>
  )
}

export default App
