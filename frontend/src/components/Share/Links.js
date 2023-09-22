import styles from "./links.module.scss"
import Button from "../common/Button"

export default function Links(props) {
    return (
        <div className={styles.links_container}>
            <p>URLリンク</p>
            <div className={styles.change_input_num}>
                <Button
                    clickFunc={() => props.addInput("links")}
                    href={undefined}
                    className="plus_button"
                >+</Button>
                <Button
                    clickFunc={() => props.reduceInput("links")}
                    href={undefined}
                    className="minus_button"
                >-</Button>
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