import React from "react"
import { useState, useEffect, useContext } from "react"
import Post from "../components/common/Post"
import Loading from "components/common/Loading"
import { useParams } from 'react-router-dom'
import { UserinfoContext } from "../App"
import signOut from "../components/functional/sign_out"
import get_user_post from "../components/functional/get_user_post"
import get_user_info from "../components/functional/get_user_info"
import styles from "./user.module.scss"

const add_page = 10
function User() {
    const { display_name } = useParams();
    const { myUserinfo, _ } = useContext(UserinfoContext)
    const [isLoading, setIsLoading] = React.useState(true)
    const [notExistFlag, setNotExistFlag] = React.useState(false)
    const [imgurl, setImgurl] = useState("")
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(0);
    const fetchPost = async (start) => {
        const data = await get_user_post(display_name, start, add_page)
        setPosts((prev) => {
            //useEffectが二回呼ばれるため（開発時）,同じ投稿が追加されるのを防ぐ
            const prevJSON = JSON.stringify(prev.slice(-data.length))
            const dataJSON = JSON.stringify(data)
            if (prevJSON !== dataJSON) return [...prev, ...data]
            else return prev
        })
    }
    const fetchIcon = async (display_name) => {
        const fetch_result = await get_user_info(display_name)
        if (fetch_result.status === 200) {
            const fetchUserinfo = await fetch_result.json()
            setImgurl(fetchUserinfo.icon_url)
        }
        else {
            setNotExistFlag(true)
        }

        setTimeout(() => {
            setIsLoading(false)
        }, 500)

    }
    useEffect(() => {
        fetchPost(page);
    }, [page]);

    useEffect(() => {
        fetchIcon(display_name)
    }, [])

    if (isLoading || myUserinfo === undefined) {
        return (
            <Loading />
        )
    }
    else if (notExistFlag) {
        return (
            <h1>User {display_name} Does Not Exist</h1>
        )
    }
    else {
        let userActionContainer = (<></>)
        if (myUserinfo.display_name === display_name) {
            userActionContainer = (
                <div className={styles.user_action_items}>
                    <a href="/user/settings">設定</a>
                    <a className={styles.signout} onClick={signOut}>
                        サインアウト
                    </a>
                </div>
            )
        }
        return (
            <div className={styles.userpage_container}>
                <div className={styles.userinfo_container}>
                    <img src={imgurl} width={100} height={100} />
                    <p>{display_name}</p>
                </div>
                {userActionContainer}
                <div className={styles.feed_content}>
                    <p className={styles.feeds_introduce}>これまでの投稿</p>
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
}

export default User;