import styles from "./app.module.scss"
import React, { createContext, useState, useEffect } from "react"
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import get_user_info from "components/functional/get_user_info";
import Header from "components/common/Header"
import Home from "./pages/Home"
import User from "./pages/User"
import Share from "./pages/Share"
import Settings from "./pages/Settings"

export const UserinfoContext = createContext()
export default function App() {
  const [userinfo, setUserinfo] = useState()
  useEffect(() => {
    const f = async () => {
      let data = await get_user_info()
      if (data.status === 401) window.location.href = "/accounts/login"
      data = await data.json()
      setUserinfo(data)
    }
    f()
  }, [])
  return (
    <UserinfoContext.Provider value={{ userinfo, setUserinfo }}>
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
