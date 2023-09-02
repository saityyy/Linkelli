export default async function get_user_info() {
    const csrf_url = "http://127.0.0.1:8000/api/v1/csrf/"
    const url =
        process.env.REACT_APP_API_SERVER_ORIGIN
        + "/api/v1/user/get_user_info/"
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
            headers: {
                "x-csrftoken": csrftoken["x-csrftoken"],
            },
        })
        .then((res) => {
            return res.json()
        });
    return data
}