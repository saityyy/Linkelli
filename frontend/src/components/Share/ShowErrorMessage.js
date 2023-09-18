import styles from "../Share/showErrorMessage.module.scss"
export default function ShowErrorMessage(props) {
    const errorCode = props.errorMessage.error_code
    let mes = "", extra_mes = ""
    if (errorCode === "InvalidURL") {
        mes = "不適切なURLリンクです。"
        extra_mes = `URL: ${props.errorMessage.invalid_url}`
    }
    else if (errorCode === "NoCommentError") {
        mes = "コメントが入力されていません。"
    }
    else if (errorCode === "NoKeywordError") {
        mes = "キーワードが入力されていません。"
        extra_mes = "少なくとも１つは必要です。"
    }
    else if (errorCode === "NoLinkError") {
        mes = "URLリンクが入力されていません。"
        extra_mes = "少なくとも１つは必要です。"
    }
    return (
        <div className={styles.error_message_container}>
            <p>{mes}</p>
            <p>{extra_mes}</p>
        </div >
    )
}