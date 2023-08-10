import { useSession, signIn, signOut } from "next-auth/react"
import Feed from "../components/mainpage/Feed"
import Head from "next/head"

export default function Home() {
    return (
        <>
            <Head>
                <title>app</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <Feed />
        </>
    )
}
