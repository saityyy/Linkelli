import { useState, useEffect } from "react"
import get_user_info from "../functional/get_user_info"
import styles from "./header.module.scss"

export default function Header() {
    const signInUrl =
        process.env.REACT_APP_API_SERVER_ORIGIN
        + "/accounts/google/login/"
    const common_html = (
        <a href="/" className={styles.logo_container}>
            <img src={"/logo.svg"} width={40} height={40} alt={"logo"} />
            <p>Linkelli</p>
        </a>
    )
    const [username, setUsername] = useState("loading")
    const [avator, setAvator] = useState("")
    useEffect(() => {
        const f = async () => {
            const user_data = await get_user_info()
            setUsername(user_data.display_name)
            setAvator(user_data.icon_url)
        }
        f()
    }, []);
    console.log(username)
    if (username === "loading") {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.account_content}>
                    <p>loading...</p>
                </div>
            </div>
        )
    }
    else if (username !== "Guest") {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.account_content}>
                    <div className={styles.greeting}>
                        <p>Hello,<br /> {username}!</p>
                    </div>
                    <a href={"/user/" + username.toString()} className={styles.account_icon}>
                        <img src={avator} width={40} alt="account icon" />
                    </a>
                </div>
                <div className={styles.post_button}>
                    <a href="/share">
                        Share
                    </a>
                </div>
            </div>
        )
    }
    else {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.not_signin}>
                    <p>Not Signed In</p>
                    <div className={styles.signin_button}>
                        <a href={signInUrl}>
                            Sign In
                        </a>
                    </div>
                </div>
            </div>
        )

    }
}
