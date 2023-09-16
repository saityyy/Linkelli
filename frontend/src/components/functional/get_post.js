export default async function get_post(start, num) {
    const url = process.env.REACT_APP_API_SERVER_ORIGIN
        + `/api/v1/post/get_post/?num=${num}&start=${start}`
    const data = await fetch(url,
        { mode: "cors", credentials: "include" })
        .then((res) => res.json())
        .catch(() => {
            const res = { posts: [] }
            for (var i = 0; i < num; i++) {
                //res.posts.append({ "id": start + i, "post": "test" })
                res.posts = [...res.posts, { "id": start + i, "post": "test" }]
            }
            return res
        })
    return data
}