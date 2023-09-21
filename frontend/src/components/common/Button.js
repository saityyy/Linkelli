import styles from "./button.module.scss"

export default function Button(props) {
    return (
        <button
            className={styles.button}
            onClick={() => props.clickFunc}>
            {props.text}
        </button>
    )

}