import React from "react"
import { useState, useEffect } from "react"
import Post from "../components/common/Post"
import { useParams } from 'react-router-dom'
import signOut from "../components/functional/sign_out"
import get_user_post from "../components/functional/get_user_post"
import styles from "./user.module.scss"

function User() {
    const { display_name } = useParams();
    const add_page = 2
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(0);
    const fetchPost = async (start) => {
        const data = await get_user_post(display_name, start, add_page)
        console.log(data)
        setPosts((prev) => {
            //useEffectが二回呼ばれるため（開発時）,同じ投稿が追加されるのを防ぐ
            const prevJSON = JSON.stringify(prev.slice(-data.length))
            const dataJSON = JSON.stringify(data)
            if (prevJSON !== dataJSON) return [...prev, ...data]
            else return prev
        })
    }
    useEffect(() => {
        fetchPost(page);
    }, [page]);

    return (
        <div>
            <h1>user name: {display_name}</h1>
            <p onClick={signOut}>sign out</p>
            <a href="/user/settings">Settings</a>
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

export default User;