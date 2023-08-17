export default async function set_user_info(body) {
    url = "http://127.0.0.1:8000/api/v1/user/ex/set_user_info/"
    const csrftoken = await fetch("http://127.0.0.1:8000/api/csrf/", {
        mode: "cors",
        credentials: "include",
    })
        .then((res) => res.json())
    const data = await fetch("",
        {
            mode: "cors",
            credentials: "include",
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "x-csrftoken": csrftoken["x-csrftoken"],
            },
            body: JSON.stringify(body)
        })
        .then((res) => res.json())
    return data
}