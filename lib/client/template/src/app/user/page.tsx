import { redirect } from 'next/navigation'

import { auth } from '@/auth'
import { NavBar } from '@/components/nav-bar'

import { SignOutButton } from './signout-btn'
import { WhoAmI } from './whoami'

export default async function PrivatePage() {
  async function whoAmI() {
    'use server'
    const session = await auth()

    if (!session?.user) {
      redirect('/sign-in?next=/user')
    }

    return session.user
  }

  return (
    <>
      <NavBar />
      <section className="flex flex-col space-y-4 container mx-auto pt-8">
        <h1 className="text-4xl">User Page</h1>
        <WhoAmI action={whoAmI} />
        <SignOutButton />
      </section>
    </>
  )
}
