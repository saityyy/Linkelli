import React from "react"
import { useParams } from 'react-router-dom'

function User() {
    const { userName } = useParams();
    const SIGNOUT_URL = process.env.REACT_APP_API_SERVER_ORIGIN
        + "/accounts/logout/"

    const signOut = async () => {
        const url = "http://127.0.0.1:8000/accounts/logout/"
        const csrftoken = await fetch("http://127.0.0.1:8000/api/csrf/", {
            mode: "cors",
            credentials: "include",
        })
            .then((res) => res.json())
        console.log(csrftoken["x-csrftoken"])
        const response = await fetch(url,
            {
                mode: "cors",
                credentials: "include",
                method: "POST",
                redirect: "manual",
                headers: {
                    "x-csrftoken": csrftoken["x-csrftoken"],
                },
            })
        console.log(response)
        window.location.href = "/"
    }

    return (
        <div>
            <h1>user name: {userName}</h1>
            <p onClick={signOut}>sign out</p>
            <a href="/user/settings">Settings</a>

        </div>
    )
}

export default User;