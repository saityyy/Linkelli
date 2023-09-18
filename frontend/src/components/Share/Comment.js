import styles from "./comment.module.scss"

export default function Comment(props) {
    return (
        <div className={styles.comment_container}>
            <p>コメント</p>
            <textarea className={"comment_0"}
                name="comment"
                cols="50"
                rows="4"
                value={props.comment}
                onChange={(props.onChange)} />
        </div>
    )
}