export default async function get_post(display_name, start, num) {
    console.log(display_name)
    const data = await fetch(
        `http://127.0.0.1:8000/api/v1/post/${display_name}/get_user_post/?num=${num}&start=${start}`,
        { mode: "cors", credentials: "include" })
        .then((res) => res.json())
        .catch(() => {
            const res = { posts: [] }
            for (var i = 0; i < num; i++) {
                res.posts = [...res.posts, { "id": start + i, "post": "test" }]
            }
            return res
        })
    return data
}