import styles from "./showErrorMessage.module.scss"
export default function ShowErrorMessage(props) {
    const errorCode = props.errorMessage.error_code
    let mes = "", extra_mes = ""
    if (errorCode === "TooBigImageSize") {
        mes = "画像のファイルサイズが大きすぎます。"
        extra_mes="300KB以下になるようにしてください。"
    }
    else if (errorCode === "InvalidFileType") {
        mes = "不適切なファイルです。"
        extra_mes="png,jpg,gif形式の画像を選択してください。"
    }
    else if (errorCode === "NotExistDisplayName") {
        mes = "ユーザー名が入力されていません。"
    }
    else if (errorCode === "DuplicateDisplayName") {
        mes = "すでに存在するユーザー名です。"
    }
    else if (errorCode === "InvalidDisplayName") {
        mes = "使えないユーザー名です。"
        extra_mes="英数字とアンダーバー（_）のみ使用可能です。長さは20文字までです。"
    }
    else{
        mes=errorCode
    }
    return (
        <div className={styles.error_message_container}>
            <p>{mes}</p>
            <p>{extra_mes}</p>
        </div >
    )
}