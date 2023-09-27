import styles from "./showErrorMessage.module.scss"
export default function ShowErrorMessage(props) {
    const errorCode = props.errorMessage.error_code
    let mes = "", extra_mes = ""
    if (errorCode === "InvalidURL") {
        mes = "不適切なURLリンクです。"
        extra_mes="URLの文字列が正しいかどうか、httpsであるかどうかを確認してください。"
    }
    else if (errorCode === "NoComment") {
        mes = "コメントが入力されていません。"
    }
    else if (errorCode === "NoKeyword") {
        mes = "キーワードが入力されていません。"
        extra_mes = "少なくとも１つは必要です。"
    }
    else if (errorCode === "NoLink") {
        mes = "URLリンクが入力されていません。"
        extra_mes = "少なくとも１つは必要です。"
    }
    else if(errorCode==="TooLongComment")mes = "コメントが長すぎます。"
    else if(errorCode==="TooLongKeyword")mes = "キーワードが長すぎます。"
    else if(errorCode==="DuplicateLink"){
        mes = "同じURLリンクが複数あります。"
        extra_mes="一個だけになるように削除、または書き換えてください。"
    }
    else if(errorCode==="DuplicateKeyword"){
        mes = "同じキーワードが複数あります。"
        extra_mes="一個だけになるように削除、または書き換えてください。"
    }
    else if(errorCode==="BadRequest"){
        mes="投稿に失敗しました。"
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