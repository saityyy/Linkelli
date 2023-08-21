import React from "react"
import styles from "./settings.module.scss"
import set_user_info from "components/functional/set_user_info"

export default function Settings() {
    const [userInfo, setUserInfo] =
        React.useState({ "display_name": "" })
    const [errMsg, setErrMsg] = React.useState("")
    const imageRef = React.useRef(null)
    const send_user_info = async () => {
        let formData = new FormData()
        formData.set("icon_image_file", imageRef.current.files[0])
        Object.keys(userInfo).map((k) => {
            formData.set(k, userInfo[k])
        })
        console.log(formData)
        const response = await set_user_info(formData)
        if (response.ok) window.location.href = "/"
        else {
            setErrMsg(response.body.error_code)
        }
    }
    const onChange = (event) => {
        console.log(imageRef)
        if (event.target.className == "display_name") {
            setUserInfo((prev) => {
                let ret = { ...prev }
                ret.display_name = event.target.value
                return ret
            })
        }
    }

    return (
        <div>
            <h1>settings</h1>
            <p>{errMsg}</p>
            <div>
                <p>display name</p>
                <input className="display_name" type="text" name="display_name" value={userInfo.display_name} onChange={onChange} />
            </div>
            <div>
                <p>icon image</p>
                <input className="icon_image" type="file" name="icon_image"
                    accept="image/png,image/jpeg"
                    ref={imageRef} onChange={onChange}
                />
            </div>
            <div>
                <p onClick={send_user_info}>
                    create account
                </p>
            </div>
        </div>
    )
}