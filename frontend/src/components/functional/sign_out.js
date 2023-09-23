export default async function SignOut() {
    const csrf_url = "/api/v1/csrf/"
    const url = "/accounts/logout/"
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
            redirect: "manual",
            headers: {
                "x-csrftoken": csrftoken["x-csrftoken"],
            },
        })
    window.location.href = "/accounts/login"
}