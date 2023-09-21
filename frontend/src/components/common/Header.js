import { useState, useEffect, useContext } from "react"
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
    const { myUserinfo, _ } = useContext(UserinfoContext)
    if (myUserinfo === undefined) {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.account_content}>
                    <p>loading...</p>
                </div>
            </div>
        )
    }
    else {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.account_content}>
                    <div className={styles.greeting}>
                        <p>Hello,<br /> {myUserinfo.display_name}!</p>
                    </div>
                    <a href={"/user/" + myUserinfo.display_name.toString()} className={styles.account_icon}>
                        <img src={myUserinfo.icon_url} width={40} alt="account icon" />
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
}
