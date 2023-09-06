export default async function get_post(keyword, start, num) {
    const url = process.env.REACT_APP_API_SERVER_ORIGIN
        + `/api/v1/set_post/get_keyword_post/?num=${num}&start=${start}&keyword=${keyword}`
    const data = await fetch(
        url,
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