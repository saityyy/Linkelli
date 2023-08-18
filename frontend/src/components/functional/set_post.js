export default async function set_post(body) {
    const url = "http://127.0.0.1:8000/api/v1/post/ex/set_post/"
    const csrftoken = await fetch("http://127.0.0.1:8000/api/csrf/", {
        mode: "cors",
        credentials: "include",
    })
        .then((res) => res.json())
    console.log(csrftoken["x-csrftoken"])
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
    return response
}