export default async function get_post(keyword,start, num) {
    let keyword_query=""
    if(keyword)keyword_query=`&keyword=${keyword}`
    const url = process.env.REACT_APP_API_SERVER_ORIGIN+ `/api/v1/post/get_post/?num=${num}&start=${start}`+keyword_query
    const data = await fetch(url,
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