import styles from "./app.module.scss"
import React from "react"
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from "components/common/Header"
import Home from "./pages/Home"
import User from "./pages/User"
import Share from "./pages/Share"

function App() {
  return (
    <div className={styles.main_container}>
      <header>
        <Header />
      </header>
      <main>
        <Router>
          <Routes>
            <Route path="" element={<Home />} />
            <Route path="share" element={<Share />} />
            <Route path=":userName" element={<User />} />
          </Routes>
        </Router>
      </main>
    </div>
  );
}

export default App;
