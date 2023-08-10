import Image from "next/image"
import styles from "./header.module.scss"
import { useState, useEffect } from "react"
import { cookies } from "next/dist/client/components/headers";
import { getCookieParser } from "next/dist/server/api-utils";
import css from "styled-jsx/css";

async function userSignIn() {
    const csrftoken = await fetch("http://127.0.0.1:8000/api/csrf/", {
        mode: "cors",
        credentials: "include",
    })
        .then((res) => res.json())

    const data = await fetch("http://127.0.0.1:8000/api/auth/get_user_profile/",
        {
            method: "GET",
            mode: "cors",
            credentials: 'include',
            redirect: 'follow',
            headers: {
                "x-csrftoken": csrftoken["x-csrftoken"],
            },
        })
        .then((res) => {
            if (res.redirected) window.location.href = res.url
            return res.json()
        })
        .then((json_data) => {
            if (json_data.extra_data == "") return json_data
            json_data.extra_data =
                JSON.parse(json_data.extra_data.replaceAll("'", "\""))
            return json_data
        });
    console.log(data)
    return data
}
export default function Header() {
    const session = 0
    const common_header = (
        <div className={styles.title_content}>
            <div className={styles.logo}>
                <Image src={"/logo.svg"} width={40} height={40} alt={"logo"} />
            </div>
            <div className={styles.title}>
                <p>Linkelli</p>
            </div>
        </div>
    )
    const [username, setUsername] = useState("")
    const [avator, setAvator] = useState("")
    useEffect(() => {
        const f = async () => {
            const user_data = await userSignIn()
            if (user_data.extra_data != "") {
                setUsername(user_data.extra_data.name)
                setAvator(user_data.extra_data.picture)
            }
            else {
                setUsername("Guest")
                setAvator("/images/guest.png")
            }
        }
        f()
    }, []);
    if (username != "") {
        return (
            <div className={styles.header}>
                {common_header}
                <button onClick={() => window.location.href = "http://127.0.0.1:8000/accounts/google/login/"}>Sign out</button>
                <div className={styles.account_content}>
                    <div className={styles.greeting}>
                        <p>Hello, {username}!</p>
                    </div>
                    <a href="/" className={styles.account_icon}>
                        <Image src={avator} width={40} height={40} alt="google account image" />
                    </a>
                    <a href="http://127.0.0.1:8000/accounts/google/login/">Sign in</a>
                </div>
            </div>
        )
    }
    return (
        <div className={styles.header}>
            {common_header}
            <div className={styles.account_content}>
                Not signed in <br />
                <a href="http://127.0.0.1:8000/accounts/google/login/">Sign in</a>
            </div>
        </div>
    )
}