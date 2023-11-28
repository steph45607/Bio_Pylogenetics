import './App.css';
import Main from "./components/Main";
import {BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Main/>}/>
      </Routes>
    </Router>
  );
}

export default App;
