export default async function get_user_info() {
    const csrf_url = "http://127.0.0.1:8000/api/csrf/"
    const url =
        process.env.REACT_APP_API_SERVER_ORIGIN
        + "/api/v1/user/ex/get_user_profile/"
    const csrftoken = await fetch(csrf_url, {
        mode: "cors",
        credentials: "include",
    })
        .then((res) => res.json())

    const data = await fetch(url,
        {
            method: "GET",
            mode: "cors",
            credentials: 'include',
            redirect: 'follow',
            headers: {
                "x-csrftoken": csrftoken["x-csrftoken"],
            },
        })
        .then((res) => {
            if (res.redirected) window.location.href = res.url
            return res.json()
        });
    if (data.redirect) window.location.href = data.redirect
    console.log(data)
    return data
}