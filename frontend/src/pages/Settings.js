import React, { useContext } from "react"
import styles from "./settings.module.scss"
import set_user_info from "components/functional/set_user_info"
import get_user_info from "components/functional/get_user_info"
import Loading from "components/common/Loading"
import Switch from "components/common/Switch"
import { useSearchParams } from "react-router-dom"
import { UserinfoContext } from "App"

export default function Settings() {
    const [isLoading, setIsLoading] = React.useState(true)
    const [isAnonymous, setIsAnonymous] = React.useState(false)
    const [userInfo, setUserInfo] = React.useState({ "display_name": "", "anonymous_mode": false })
    const [iconImage, setIconImage] = React.useState("/logo192.png")
    const [errMsg, setErrMsg] = React.useState("")
    const imageRef = React.useRef(null)
    const [searchParams, setSearchParams] = useSearchParams()
    const redirect_url = searchParams.get("redirect")
    const send_user_info = async () => {
        let formData = new FormData()
        formData.set("icon_image_file", imageRef.current.files[0])
        Object.keys(userInfo).map((k) => {
            formData.set(k, userInfo[k])
        })
        const response = await set_user_info(formData)
        if (response.ok) window.location.href = "/"
        else {
            setErrMsg(response.body.error_code)
        }
    }
    const changeUserinfoField = (fieldName, targetValue) => {
        setUserInfo((prev) => {
            let ret = { ...prev }
            ret[fieldName] = targetValue
            return ret
        })
    }
    const onChange = (event) => {
        const className = event.target.className
        if (className === "icon_image") {
            if (!event.target.files) return
            const fileObject = event.target.files[0]
            setIconImage(window.URL.createObjectURL(fileObject))
        }
        else {
            let inputValue = event.target.value
            if (event.target.type === "checkbox")
                inputValue = event.target.checked
            changeUserinfoField(className, inputValue)
        }
    }
    const { userinfo, _ } = useContext(UserinfoContext)
    if (userinfo !== undefined && isLoading) {
        const is_exist_user_info = userinfo.exist_user_info
        if (is_exist_user_info && redirect_url)
            window.location.href = "/"
        else {
            setIsLoading(false)
            changeUserinfoField("anonymous_mode", userinfo.anonymous_mode)
        }
    }
    if (isLoading) return (
        <div>
            <Loading />
        </div>
    )
    else {
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
                    <img src={iconImage} width={50} height={50} />
                </div>
                <div>
                    <p>Anonymous Mode</p>
                    <Switch
                        init_value={userInfo.anonymous_mode}
                        onChange={onChange}
                        className={"anonymous_mode"}
                    />
                    {userInfo.anonymous_mode &&
                        <p>In this mode, all your personal information is hidden.</p>
                    }
                </div>
                <div>
                    <p onClick={send_user_info}>
                        create account
                    </p>
                </div>
            </div>
        )
    }
}