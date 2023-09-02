import styles from "./switch.module.scss"
import { useRef } from "react"

export default function Switch(props) {
    const isAnonymous = props.init_value
    console.log(isAnonymous)
    return (
        <label for="switch" className={styles.anonymous_mode}>
            <div className={styles.switch}>
                <input
                    type="checkbox"
                    id="switch"
                    className={props.className}
                    onChange={props.onChange}
                    defaultChecked={isAnonymous}
                />
                <div className={styles.circle}></div>
                <div className={styles.base}></div>
            </div>
        </label>
    )
}