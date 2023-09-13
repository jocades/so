'use client'

import { useState } from 'react'
import { Session } from 'next-auth'

import { Button } from '@/components/ui/button'

interface WhoAmIProps {
  action: () => Promise<Session['user']>
}

export function WhoAmI({ action }: WhoAmIProps) {
  const [user, setUser] = useState<Session['user']>()

  return (
    <div>
      <Button onClick={async () => setUser(await action())}>Who Am I?</Button>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </div>
  )
}
