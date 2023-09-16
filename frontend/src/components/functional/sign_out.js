export default async function SignOut() {
    const csrf_url = process.env.REACT_APP_API_SERVER_ORIGIN
        + "/api/v1/csrf/"
    const url = process.env.REACT_APP_API_SERVER_ORIGIN
        + "/accounts/logout/"
    const csrftoken = await fetch(csrf_url, {
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
            redirect: "manual",
            headers: {
                "x-csrftoken": csrftoken["x-csrftoken"],
            },
        })
    console.log(response)
    window.location.href = "/"
}