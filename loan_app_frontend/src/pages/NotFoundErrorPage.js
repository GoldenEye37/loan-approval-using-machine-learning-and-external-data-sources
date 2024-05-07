

export default function NotFoundErrorPage() {
    return (
        <main className="flex items-stretch h-screen min-h-full  place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8">
            <div className="text-center self-center mx-auto">
                <p className="text-base font-semibold text-indigo-600">404</p>
                <h1 className="mt-4 font-bold tracking-tight text-green-400 sm:text-5xl">Page not found</h1>
                <p className="mt-6 text-base leading-7 text-gray-600">Sorry, we couldn’t find the page you’re looking
                    for.</p>
                <div className="mt-10 flex items-center justify-center gap-x-6">
                    <a
                        href="#"
                        className="self-center rounded-full align-middle bg-gradient-to-r from-indigo-600 to-pink-500 px-5 py-3 text-sm font-semibold
                    text-white shadow-sm drop-shadow-md hover:drop-shadow-2xl focus-visible:outline focus-visible:outline-2
                    focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    >
                        Go to Home
                    </a>
                </div>
            </div>
        </main>)
}