import styles from "./links.module.scss"

export default function Links(props) {
    return (
        <div className={styles.links_container}>
            <p>URLリンク</p>
            <div className={styles.change_input_num}>
                <button onClick={() => props.addInput("links")}>+</button>
                <button onClick={() => props.reduceInput("links")}>-</button>
            </div>
            <ul>
                {props.links.map((link, i) => (
                    <li key={i.toString()}>
                        <textarea className={"links_" + i.toString()}
                            name="link" value={link.link} onChange={props.onChange} />
                    </li>
                ))}
            </ul>
        </div>
    )
}