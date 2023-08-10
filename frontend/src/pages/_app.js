import { SessionProvider } from "next-auth/react"
import "/src/styles/globals.css"
import Header from "../components/layouts/Header"
import { useLayoutEffect } from "react"

export default function App({ Component, pageProps }) {
    return (
        <>
            <Header />
            <Component {...pageProps} />
        </>
    )
}