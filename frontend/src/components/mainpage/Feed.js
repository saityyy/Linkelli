import { useState, useEffect } from "react"
import Posts from "../ui/Post";
import styles from "./feed.module.scss"

export default function Home() {
    const add_page = 10
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(0);
    const fetchPost = async (start) => {
        const data = await fetch(`http://127.0.0.1:8000/api/v1/get_post/?num=${add_page}&start=${start}`,
            { mode: "cors", credentials: "include" })
            .then((res) => res.json())
            .catch(() => {
                const res = { posts: [] }
                for (var i = 0; i < add_page; i++) {
                    //res.posts.append({ "id": start + i, "post": "test" })
                    res.posts = [...res.posts, { "id": start + i, "post": "test" }]
                }
                return res
            })
        console.log(data)
        setPosts((prev) => [...prev, ...data])
        console.log(`posts.length${posts.length}`)
    }
    useEffect(() => {
        if (page < 3) fetchPost(page);
    }, [page])
    return (
        <div>
            <div className={styles.feed_content}>
                {posts.map((post, index) => (
                    <Posts
                        post={post}
                        newLimit={() => setPage(page + add_page)}
                        isLast={index === posts.length - 1}
                        key={post.post_id} />
                ))}
            </div>
        </div>
    )
}
