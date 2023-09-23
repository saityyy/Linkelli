export default async function set_user_info(body) {
    const csrf_url = process.env.REACT_APP_API_SERVER_ORIGIN
        + "/api/v1/csrf/"
    const url = process.env.REACT_APP_API_SERVER_ORIGIN
        + "/api/v1/user/set_user_info/"
    const csrftoken = await fetch(csrf_url, {
        mode: "cors",
        credentials: "include",
    })
        .then((res) => res.json())
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