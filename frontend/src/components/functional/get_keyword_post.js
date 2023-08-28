export default async function get_post(keyword, start, num) {
    console.log(keyword)
    const data = await fetch(
        `http://127.0.0.1:8000/api/v1/set_post/get_keyword_post/?num=${num}&start=${start}&keyword=${keyword}`,
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