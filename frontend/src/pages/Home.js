import React from 'react'
import { useState, useEffect } from "react"
import Post from "../components/common/Post";
import styles from "./home.module.scss"
import get_post from "../components/functional/get_post";
import get_keyword_post from "../components/functional/get_keyword_post";
import { useSearchParams } from "react-router-dom"

export default function Home() {
    const add_page = 2
    const [posts, setPosts] = useState([]);
    let [searchParams, setSearchParams] = useSearchParams()
    const [page, setPage] = useState(0);
    const fetchPost = async (start) => {
        let data = []
        if (searchParams.get("keyword")) {
            data = await get_keyword_post(
                searchParams.get("keyword"), start, add_page)
        }
        else {
            data = await get_post(start, add_page)
        }
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
