export default async function get_post(start, num) {
    const data = await fetch(`http://127.0.0.1:8000/api/v1/post/get_post/?num=${num}&start=${start}`,
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