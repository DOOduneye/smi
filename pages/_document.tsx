import { Html, Head, Main, NextScript } from 'next/document';

const Document = () => {
    return (
        <Html lang="en" className="h-full">
        <Head>
            <meta name="description" content="SMI" />
            <link rel="icon" href="/favicon.ico" />
        </Head>
        <body className="bg-white h-full">
            <Main />
            <NextScript />
        </body>
        </Html>
    );
};

export default Document;