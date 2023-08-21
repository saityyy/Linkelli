import React from "react"
import set_post from "../components/functional/set_post"
import styles from "./share.module.scss"
import Keywords from "../components/Share/Keywords"
import Links from "../components/Share/Links"
import Comment from "../components/Share/Comment"

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
    const addInput = (input_content) => {
        setFormdata((prev) => {
            if (prev[input_content].length >= 5) return prev
            const ret = JSON.parse(JSON.stringify(prev))//deep copy
            let new_input = {}
            if (input_content === "keywords") new_input.keyword = ""
            if (input_content === "links") new_input.link = ""
            ret[input_content].push(new_input)
            localStorage.setItem("formdata", JSON.stringify(ret))
            return ret
        })
    }
    const reduceInput = (input_content) => {
        setFormdata((prev) => {
            if (prev[input_content].length === 1) return prev
            const ret = JSON.parse(JSON.stringify(prev))//deep copy
            ret[input_content].pop()
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
        <div className={styles.share_container}>
            <p>Share</p>
            <Comment
                comment={formdata.comment}
                onChange={onChange} />
            <Keywords
                keywords={formdata.keywords}
                addInput={addInput}
                reduceInput={reduceInput}
                onChange={onChange} />
            <Links
                links={formdata.links}
                addInput={addInput}
                reduceInput={reduceInput}
                onChange={onChange} />
            <div className={styles.send_post_button}>
                <p onClick={send_post}>
                    Share your linkelli
                </p>
            </div>
        </div>
    )
}
