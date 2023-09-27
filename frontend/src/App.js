import styles from "./app.module.scss"
import React, { createContext, useState, useEffect } from "react"
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import get_my_info from "components/functional/get_my_info";
import Header from "components/common/Header"
import Home from "./pages/Home"
import User from "./pages/User"
import Share from "./pages/Share"
import Settings from "./pages/Settings"

export const UserinfoContext = createContext()
export default function App() {
  const [myUserinfo, setMyUserinfo] = useState()
  useEffect(() => {
    const f = async () => {
      let data = await get_my_info()
      if (data.status === 403) window.location.href = "/accounts/login"
      data = await data.json()
      setMyUserinfo(data)
    }
    f()
  }, [])
  return (
    <UserinfoContext.Provider value={{ myUserinfo, setMyUserinfo }}>
      <div className={styles.main_container}>
        <header>
          <Header />
        </header>
        <main>
          <Router>
            <Routes>
              <Route path="" element={<Home />} />
              <Route path="share" element={<Share />} />
              <Route path="user/settings" element={<Settings />} />
              <Route path="user/:display_name" element={<User />} />
            </Routes>
          </Router>
        </main>
      </div>
    </UserinfoContext.Provider>
  );
};
