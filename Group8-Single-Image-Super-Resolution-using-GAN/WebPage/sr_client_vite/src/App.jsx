// import React, { useEffect, useState } from "react";
// import axios from "axios";
import "./App.css";
import React, { useState } from 'react';
import { BrowserRouter as Router,Route,Routes,Navigate} from 'react-router-dom';
import Landing from "/src/components/Landing";
import Home from "/src/components/Home";
import Register from "/src/components/Register";
import ForgetPassword from "/src/components/ForgetPassword";
import Notfound from "/src/components/Notfound";

function App() {
  const [isAuthenticated, setAuthenticated] = useState(false);

  return (
    <Router>
      <div className="App">
        <Routes>
        <Route path="/" element={<Landing setAuthenticated={setAuthenticated} />} />
          <Route path="/register" element={<Register/>} />
          <Route path="/forget-password" element={<ForgetPassword/>} />
          <Route
            path="/home"
            element={isAuthenticated ? <Home /> : <Navigate to="/" />}
          />
          <Route path="*" element={<Notfound/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
