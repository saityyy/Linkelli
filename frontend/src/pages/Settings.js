import { useState, useRef, useEffect, useContext } from "react"
import styles from "./settings.module.scss"
import set_user_info from "components/functional/set_user_info"
import Loading from "components/common/Loading"
import Button from "components/common/Button"
import Switch from "components/common/Switch"
import { useSearchParams } from "react-router-dom"
import { UserinfoContext } from "App"

export default function Settings() {
    const [isLoading, setIsLoading] = useState(true)
    const [userInfo, setUserInfo] = useState({ "display_name": "", "anonymous_mode": false })
    const [iconImageURL, setIconImageURL] = useState("/logo192.png")
    const [errMsg, setErrMsg] = useState("")
    const { myUserinfo, _ } = useContext(UserinfoContext)
    const imageRef = useRef(null)
    const [searchParams, setSearchParams] = useSearchParams()
    const redirect_url = searchParams.get("redirect")
    const send_user_info = async () => {
        let formData = new FormData()
        if (myUserinfo.icon_url === iconImageURL) {
            const noChangeImage = await fetch(myUserinfo.icon_url)
                .then((res) => res.blob())
            const noChangeImageFile = new File([noChangeImage], "icon.png", { type: "image/png" })
            formData.set("icon_image_file", noChangeImageFile)
        }
        else {
            formData.set("icon_image_file", imageRef.current.files[0])
        }
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
            setIconImageURL(window.URL.createObjectURL(fileObject))
        }
        else {
            let inputValue = event.target.value
            if (event.target.type === "checkbox")
                inputValue = event.target.checked
            changeUserinfoField(className, inputValue)
        }
    }
    useEffect(() => {
        const preprocess = async () => {
            if (myUserinfo !== undefined && isLoading) {
                const is_exist_user_info = myUserinfo.exist_user_info
                if (is_exist_user_info && redirect_url)
                    window.location.href = "/"
                else {
                    setIconImageURL(myUserinfo.icon_url)
                    setTimeout(() => {
                        setIsLoading(false)
                        console.log(myUserinfo)
                        changeUserinfoField("anonymous_mode", myUserinfo.anonymous_mode)
                        changeUserinfoField("display_name", myUserinfo.display_name)
                    }, 500)
                }
            }
        }
        preprocess()
    }, [myUserinfo, imageRef])
    if (isLoading) return (
        <div>
            <Loading />
        </div>
    )
    else {
        return (
            <div className={styles.settings_container}>
                <h1>ユーザー設定</h1>
                <p>{errMsg}</p>
                <div className={styles.setting_display_name}>
                    <p className={styles.setting_item_name}>ユーザー名</p>
                    <label htmlFor="display_name">
                        <input id="display_name"
                            className="display_name"
                            type="text"
                            name="display_name"
                            value={userInfo.display_name}
                            onChange={onChange}
                        />
                    </label>
                </div>
                <div className={styles.setting_icon_image}>
                    <p className={styles.setting_item_name}>アイコン画像</p>
                    <label>
                        <input className="icon_image" type="file" name="icon_image"
                            accept="image/png,image/jpeg"
                            ref={imageRef} onChange={onChange}
                        />
                        <img src={iconImageURL} />
                    </label>
                </div>
                <div className={styles.setting_anonymous_mode}>
                    <p className={styles.setting_item_name}>匿名モード</p>
                    <Switch
                        init_value={userInfo.anonymous_mode}
                        onChange={onChange}
                        className={"anonymous_mode"}
                    />
                    <p className={styles[`anonymous_${myUserinfo.anonymous_mode}`]}>匿名モードをONにするとあなたのユーザー情報は他のユーザーから見られることがなくなります。
                    </p>
                </div>
                <Button
                    clickFunc={send_user_info}
                    href={undefined}
                    className={`${styles.change_settings_button}`}>
                    設定を変更する
                </Button >
            </div>
        )
    }
}