import React from "react"
import set_post from "../components/functional/set_post"
import styles from "./share.module.scss"

export default function Share() {
    let formdata_ini = localStorage.getItem("formdata")
    if (!formdata_ini) {
        formdata_ini = JSON.stringify({
            "keywords": [{ "keyword": "test" }],
            "links": [{ "link": "https://saity.dev" }],
            "comment": "test share"
        })
        localStorage.setItem("formdata", formdata_ini)
    }
    formdata_ini = JSON.parse(formdata_ini)
    const [formdata, setFormdata] =
        React.useState(formdata_ini)
    const onChange = (event) => {
        const input_content = event.target.className.split("_")[0]
        const idx = event.target.className.split("_")[1]
        setFormdata((prev) => {
            const ret = JSON.parse(JSON.stringify(prev))//deep copy
            if (idx === "none") ret[input_content] = event.target.value
            else if (input_content === "keywords")
                ret.keywords[parseInt(idx)].keyword = event.target.value
            else if (input_content === "links")
                ret.links[parseInt(idx)].link = event.target.value
            console.log(ret)
            localStorage.setItem("formdata", JSON.stringify(ret))
            return ret;
        })
    }
    const add_input = (input_content) => {
        setFormdata((prev) => {
            const ret = JSON.parse(JSON.stringify(prev))//deep copy
            let new_input = {}
            if (input_content === "keywords") new_input.keyword = ""
            if (input_content === "links") new_input.link = ""
            ret[input_content].push(new_input)
            localStorage.setItem("formdata", JSON.stringify(ret))
            return ret
        })
    }

    const send_post = async () => {
        let body = JSON.parse(localStorage.getItem("formdata"))
        body.keywords = body.keywords.filter((k) => k.keyword !== "")
        body.links = body.links.filter((l) => l.link !== "")
        console.log(body)
        const response = await set_post(body)
        console.log(response)
        if (response.status === 200) window.location.href = "/"
    }

    return (
        <div>
            <h1>Share</h1>
            <div>
                <p>input comment</p>
                <input className={"comment_none"}
                    type="text" name="comment" value={formdata.comment} onChange={(onChange)} />
            </div>
            <div>
                <p>input keywords</p>
                <div>
                    <button onClick={() => add_input("keywords")}>add input form</button>
                    <ul>
                        {formdata.keywords.map((keyword, i) => (
                            <li key={i.toString()}>
                                <input className={"keywords_" + i.toString()}
                                    type="text" name="keyword" value={keyword.keyword} onChange={onChange} />
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
            <div>
                <p>input url link</p>
                <div>
                    <button onClick={() => add_input("links")}>add input form</button>
                    <ul>
                        {formdata.links.map((link, i) => (
                            <li key={i.toString()}>
                                <input className={"links_" + i.toString()}
                                    type="text" name="link" value={link.link} onChange={onChange} />
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
            <div className={styles.send_post_button}>
                <p onClick={send_post}>
                    Share your linkelli
                </p>
            </div>
        </div>
    )
}
