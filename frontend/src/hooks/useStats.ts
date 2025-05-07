// frontend/src/hooks/useStats.ts
import { useEffect, useState } from 'react'

export type Stats = { completion_rate: number; missed_tasks: number; streak: number }

export const useStats = () => {
  const [stats, setStats] = useState<Stats | null>(null)

  useEffect(() => {
    const API = import.meta.env.VITE_API_URL

    const fetchStats = async () => {
      try {
        const res = await fetch(`${API}/stats`, { credentials: 'include' })
        if (res.ok) {
          const data: Stats = await res.json()
          setStats(data)
        }
      } catch (err) {
        console.error('fetch stats failed', err)
      }
    }

    fetchStats()
  }, [])

  return { stats }
}
