import styles from "./keywords.module.scss"
import Button from "../common/Button"

export default function Keywords(props) {
    return (
        <div className={styles.keywords_container}>
            <p>キーワード</p>
            <div className={styles.change_input_num}>
                <Button
                    clickFunc={() => props.addInput("keywords")}
                    href={undefined}
                    className="plus_button"
                >+</Button>
                <Button
                    clickFunc={() => props.reduceInput("keywords")}
                    href={undefined}
                    className="minus_button"
                >-</Button>
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