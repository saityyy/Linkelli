import styles from "./keywords.module.scss"

export default function Keywords(props) {
    return (
        <div className={styles.keywords_container}>
            <p>キーワード</p>
            <div className={styles.change_input_num}>
                <button onClick={() => props.addInput("keywords")}>+</button>
                <button onClick={() => props.reduceInput("keywords")}>-</button>
            </div>
            <ul>
                {props.keywords.map((keyword, i) => (
                    <li key={i.toString()}>
                        <textarea className={"keywords_" + i.toString()}
                            name="keyword" value={keyword.keyword} onChange={props.onChange} />
                    </li>
                ))}
            </ul>
        </div >
    )
}