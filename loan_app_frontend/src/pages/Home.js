import { useState } from 'react'
import { Dialog } from '@headlessui/react'

const navigation = [
  { name: 'Product', href: '#' },
  { name: 'Features', href: '#' },
  { name: 'Marketplace', href: '#' },
  { name: 'Company', href: '#' },
]

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="bg-white h-screen">
      <div className="relative h-full isolate overflow-hidden  bg-gradient-to-b from-indigo-500/20 pt-14">
        <div
          className=" absolute inset-y-0 right-1/2 -z-10 -mr-96 w-[200%] origin-top-right skew-x-[-30deg] bg-white shadow-xl shadow-indigo-600/10 ring-1 ring-indigo-50 sm:-mr-80 lg:-mr-96"
          aria-hidden="true"
        />
        <div className="mx-auto max-w-7xl px-6 py-32 sm:py-40 lg:px-8">
          <div
              className="mx-auto max-w-2xl lg:mx-0 lg:grid lg:max-w-none lg:grid-cols-2 lg:gap-x-16 lg:gap-y-6 xl:grid-cols-1 xl:grid-rows-1 xl:gap-x-8">
            <h1 className="max-w-2xl text-4xl font-bold tracking-tight sm:text-6xl lg:col-span-2 xl:col-auto
                          bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Loan Approval using ML and external news sources.
            </h1>
            <div className="mt-6 max-w-xl lg:mt-0 xl:col-end-1 xl:row-start-1">
              <p className="text-lg leading-8 text-gray-400">
                This is a loan approval system, exceptional in all aspects. It is a system that is designed to make
                loan approval using real time data and machine learning. The system uses external news to enhance the
                loan approval process, by mitigating the risk of loan default due to unforeseen circumstances. The
                system
                also promotes transparency and fairness taking into consideration how a certain industry is performing.
              </p>
              <div className="mt-10 flex items-stretch gap-x-6">
                <a
                    href="#"
                    className="self-center rounded-full align-middle bg-gradient-to-r from-indigo-600 to-pink-500 px-5 py-3 text-sm font-semibold
                    text-white shadow-sm drop-shadow-md hover:drop-shadow-2xl focus-visible:outline focus-visible:outline-2
                    focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Approve Loan
                </a>
                {/*<a href="#" className="text-sm font-semibold leading-6 text-gray-900">*/}
                {/*  Learn more <span aria-hidden="true">→</span>*/}
                {/*</a>*/}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
