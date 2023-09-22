import styles from "./button.module.scss"

export default function Button(props) {
    return (
        <a href={props.href}
            className={`${styles.button} ${props.className}`}
            onClick={() => props.clickFunc()}>
            <span>{props.children}</span>
        </a>
    )

}