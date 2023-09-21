import React from "react"
import { useEffect, useRef } from "react";
import styles from "./post.module.scss"

const Post = (({ post, newLimit, isLast }) => {
    const postRef = useRef()
    useEffect(() => {
        if (!postRef?.current) return;
        const observer = new IntersectionObserver(([entry]) => {
            if (isLast && entry.isIntersecting) {
                newLimit();
                observer.unobserve(entry.target);
            }
        });
        observer.observe(postRef.current);
    }, [isLast]);
    const y = new Date(post.created).getFullYear()
    const m = new Date(post.created).getMonth() + 1
    const d = new Date(post.created).getDate()
    const hour = new Date(post.created).getHours()
    const minute = (new Date(post.created).getMinutes()).toString().padStart(2, "0")
    const post_created_time = `${y} ${m}/${d}  ${hour}:${minute}`
    let IsAnonymous = "public_user"
    if (post.post_sender.anonymous_mode === true) {
        IsAnonymous = "anonymous_user"
    }
    return (
        <div ref={postRef} className={styles.post_container}>
            <div className={styles.poster_content}>
                <div className={`${styles.poster_info} ${styles[IsAnonymous]}`}>
                    <a href={`/user/${post.post_sender.display_name}`}>
                        <img src={post.post_sender.icon_url} width={30} height={30} alt={"website_image"} />
                    </a>
                    <a href={`/user/${post.post_sender.display_name}`}>
                        {post.post_sender.display_name}
                    </a>
                    <p>{post_created_time}</p>
                </div>
                <div className={styles.post_info}>
                    <p>
                        {post.keywords.map((keyword, index) => (
                            <span key={index.toString()}>
                                <a href={`/?keyword=${keyword.keyword}`}>#{keyword.keyword}, </a>
                            </span>
                        ))}
                    </p>
                    <p>{post.comment}</p>
                </div>
            </div>
            <div className={styles.target_contents}>
                <ul>
                    {post.links.map((link, index) => (
                        <li key={index.toString()}>
                            {/* <p>{link.link}</p> */}
                            <a href={link.link} target="_blank" referer="noopener">
                                <img src={link.img_url} width={20} height={20} alt={"website_image"} />
                                <p>{link.title}</p>
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
            <div>
            </div>
        </div >);
});

export default Post;