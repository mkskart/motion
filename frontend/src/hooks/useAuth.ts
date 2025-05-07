// frontend/src/hooks/useAuth.ts
import { useEffect, useState } from 'react'

export type User = { id: number; email: string; name: string }

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    const API = import.meta.env.VITE_API_URL
    console.log('🔍 fetching /me…', 'API =', API)

    const fetchMe = async () => {
      try {
        const res = await fetch(`${API}/me`, { credentials: 'include' })
        console.log('📥 /me status:', res.status)
        if (res.ok) {
          const u: User = await res.json()
          console.log('✅ /me user:', u)
          setUser(u)
        } else {
          console.log('⚠️ /me not ok, returning null')
          setUser(null)
        }
      } catch (err) {
        console.error('❌ /me error:', err)
        setUser(null)
      }
    }

    fetchMe()
  }, [])

  return { user }
}
