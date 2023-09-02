export default async function set_user_info(body) {
    const api_server = process.env.REACT_APP_API_SERVER_ORIGIN
    const url = api_server + "/api/v1/user/set_user_info/"
    const csrf_url = api_server + "/api/v1/csrf/"
    const csrftoken = await fetch(csrf_url, {
        mode: "cors",
        credentials: "include",
    })
        .then((res) => res.json())
    console.log(csrftoken)
    let result = {
        "ok": true,
        "body": {}

    }
    result.body = await fetch(url,
        {
            mode: "cors",
            credentials: "include",
            method: "POST",
            headers: {
                "x-csrftoken": csrftoken["x-csrftoken"],
            },
            body: body
        })
        .then(res => {
            result.ok = res.ok
            return res.json()
        })
    return result
}