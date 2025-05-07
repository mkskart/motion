// frontend/src/hooks/useTasks.ts
import { useEffect, useState } from 'react'

export type Task = {
  id: number
  title: string
  description?: string
  duration_minutes: number
  priority: 'high' | 'medium' | 'low'
  scheduled_start?: string
  scheduled_end?: string
}

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([])

  useEffect(() => {
    const API = import.meta.env.VITE_API_URL

    const load = async () => {
      try {
        const res = await fetch(`${API}/tasks`, { credentials: 'include' })
        if (res.ok) {
          const data: Task[] = await res.json()
          setTasks(data)
        }
      } catch (err) {
        console.error('fetch tasks failed', err)
      }
    }

    load()
  }, [])

  const createTask = async (t: Partial<Task>) => {
    const API = import.meta.env.VITE_API_URL
    try {
      await fetch(`${API}/tasks`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(t),
      })
      // reload after create
      const res = await fetch(`${API}/tasks`, { credentials: 'include' })
      if (res.ok) {
        setTasks(await res.json())
      }
    } catch (err) {
      console.error('create task failed', err)
    }
  }

  return { tasks, createTask }
}
