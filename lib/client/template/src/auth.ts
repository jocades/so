import NextAuth, { type DefaultSession } from 'next-auth'
import GitHubProvider from 'next-auth/providers/github'

declare module 'next-auth' {
  interface Session {
    // extend the session with custom properties
    user: {} & DefaultSession['user']
  }
}

export { getServerSession as auth } from 'next-auth'

const handler = NextAuth({
  providers: [
    GitHubProvider({
      clientId: process.env.AUTH_GITHUB_ID!,
      clientSecret: process.env.AUTH_GITHUB_SECRET!,
    }),
  ],
  pages: {
    signIn: '/sign-in',
  },
})

export { handler as GET, handler as POST }
