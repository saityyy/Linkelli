import { useState, useEffect, useContext } from "react"
import get_user_info from "../functional/get_user_info"
import styles from "./header.module.scss"
import { UserinfoContext } from "../../App"

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
    const { userinfo, _ } = useContext(UserinfoContext)
    console.log(userinfo)
    if (userinfo === undefined) {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.account_content}>
                    <p>loading...</p>
                </div>
            </div>
        )
    }
    else if (userinfo.display_name !== "Guest") {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.account_content}>
                    <div className={styles.greeting}>
                        <p>Hello,<br /> {userinfo.display_name}!</p>
                    </div>
                    <a href={"/user/" + userinfo.display_name.toString()} className={styles.account_icon}>
                        <img src={userinfo.icon_url} width={40} alt="account icon" />
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
