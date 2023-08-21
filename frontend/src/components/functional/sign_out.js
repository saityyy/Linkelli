export default async function SignOut() {
    const url = "http://127.0.0.1:8000/accounts/logout/"
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
            redirect: "manual",
            headers: {
                "x-csrftoken": csrftoken["x-csrftoken"],
            },
        })
    console.log(response)
    window.location.href = "/"
}