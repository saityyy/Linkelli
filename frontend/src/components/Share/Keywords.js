import styles from "./keywords.module.scss"

export default function Keywords(props) {
    console.log(props.keywords)
    return (
        <div>
            <p>input keywords</p>
            <div>
                <button onClick={() => props.addInput("keywords")}>+</button>
                <button onClick={() => props.reduceInput("keywords")}>-</button>
                <ul>
                    {props.keywords.map((keyword, i) => (
                        <li key={i.toString()}>
                            <input className={"keywords_" + i.toString()}
                                type="text" name="keyword" value={keyword.keyword} onChange={props.onChange} />
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}