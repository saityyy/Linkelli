import React from 'react'
import { useState, useEffect } from "react"
import Post from "../components/Home/Post";
import styles from "./home.module.scss"
import get_post from "../components/functional/get_post";

export default function Home() {
    const add_page = 1
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(0);
    const fetchPost = async (start) => {
        const data = await get_post(start, add_page)
        console.log(data)
        setPosts((prev) => [...prev, ...data])
        console.log(`posts.length${posts.length}`)
    }
    useEffect(() => {
        fetchPost(page);
    }, [page]);
    return (
        <div>
            {/* <button onClick={() => test_api("http://127.0.0.1:8000/api/v1/post/ex/set_post/", {
                "links": [
                    { "link": "https://docs.python.org/ja/3/library/urllib.parse.html" },
                    { "link": "https://qiita.com/aKuad/items/a928d6e70f1278990052" },
                    { "link": "https://zenn.dev/turing_motors/articles/6e0ac9deb2d2e5" },
                    { "link": "https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/" }
                ],
                "keywords": [
                    { "keyword": "python" },
                    { "keyword": "js" },
                    { "keyword": "LLM" },
                    { "keyword": "urlparse" },
                    { "keyword": "many-to-one_relationship" }
                ],
                "comment": "test : set_post process"
            })}>test set post </button>
            <button onClick={() => test_api("http://127.0.0.1:8000/api/v1/user/ex/set_user_info/", {
                "display_name": "abcde",
                "icon_url": "https://pbs.twimg.com/profile_images/1610819875567734785/5kM_BxFL_400x400.jpg"
            })}>test put </button> */}
            <div className={styles.feed_content}>
                {posts.map((post, index) => (
                    <Post
                        post={post}
                        newLimit={() => setPage(page + add_page)}
                        isLast={index === posts.length - 1}
                        key={index.toString()} />
                ))}
            </div>
        </div>
    )
}
