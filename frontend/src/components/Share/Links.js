import styles from "./links.module.scss"

export default function Links(props) {
    return (
        <div>
            <p>input url link</p>
            <div>
                <button onClick={() => props.addInput("links")}>+</button>
                <button onClick={() => props.reduceInput("links")}>-</button>
                <ul>
                    {props.links.map((link, i) => (
                        <li key={i.toString()}>
                            <input className={"links_" + i.toString()}
                                type="text" name="link" value={link.link} onChange={props.onChange} />
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}