import styles from "./comment.module.scss"

export default function Comment(props) {
    const formdata = props.formdata
    return (
        <div>
            <p>input comment</p>
            <input className={"comment_none"}
                type="text" name="comment" value={props.comment} onChange={(props.onChange)} />
        </div>
    )
}