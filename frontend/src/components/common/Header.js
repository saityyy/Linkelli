import { useState, useEffect, useContext } from "react"
import styles from "./header.module.scss"
import { UserinfoContext } from "../../App"
import Button from "./Button"

export default function Header() {
    const signInUrl =
        process.env.REACT_APP_API_SERVER_ORIGIN
        + "/accounts/google/login/"
    const common_html = (
        <a href="/" className={styles.logo_container}>
            <img src={"/logo.png"} width={60} height={60} alt={"logo"} />
            <p>Linkelli</p>
        </a>
    )
    const { myUserinfo, _ } = useContext(UserinfoContext)
    if (myUserinfo === undefined) {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.account_container}>
                    <p>loading...</p>
                </div>
            </div>
        )
    }
    else {
        return (
            <div className={styles.header_container}>
                {common_html}
                <div className={styles.account_container}>
                    <div className={styles.display_name}>
                        <p>
                            <span className={styles.hello}>Hello,<br />
                            </span>
                            {myUserinfo.display_name}
                        </p>
                    </div>
                    <a href={"/user/" + myUserinfo.display_name.toString()} className={styles.account_icon}>
                        <img src={myUserinfo.icon_url} width={40} alt="account icon" />
                    </a>
                </div>
                <Button
                    href="/share"
                    className={styles.post_button}
                >
                    投稿
                </Button>
            </div>
        )
    }
}
