import { useEffect, useRef } from "react";
import Image from "next/image"
import Link from "next/link"
import styles from "./post.module.scss"

const Posts = (({ post, newLimit, isLast }) => {
    const postRef = useRef()
    const keywords = ["aaaaa", "bbbbbbbbbbbbbbbbb", "cccccccc"]
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
    return (
        <div ref={postRef} className={styles.post_container}>
            <div className={styles.poster_content}>
                <div className={styles.poster_info}>
                    <Link href="/">
                        <Image src={post.poster_icon_url} width={30} height={30} alt={"website_image"} />
                    </Link>
                    <Link href="/">{post.post_sender}</Link>
                    <p>7.20 3:29</p>
                </div>
                <div className={styles.post_info}>
                    <p>
                        {post.keywords.map((keyword, index) => (
                            <span key={post.post_id + "_" + index}>
                                <Link href="/">#{keyword.keyword}, </Link>
                            </span>
                        ))}
                    </p>
                    <p>{post.comment}</p>
                </div>
            </div>
            <div className={styles.target_contents}>
                <ul>
                    {post.links.map((link, index) => (
                        <li key={post.post_id + "_" + index}>
                            <a href={link.link} target="_blank" referer="noopener">
                                <Image src={link.img_url} width={20} height={20} alt={"website_image"} />
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
export default Posts;