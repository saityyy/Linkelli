export default async function set_post(body) {
    const csrf_url = process.env.REACT_APP_API_SERVER_ORIGIN
        + "/api/v1/csrf/"
    const url = process.env.REACT_APP_API_SERVER_ORIGIN
        + "/api/v1/post/set_post/"
    const csrftoken = await fetch(csrf_url, {
        mode: "cors",
        credentials: "include",
    })
        .then((res) => res.json())
    const response = await fetch(url,
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
    //.then((res) => res.json())
    return response
}