import React, { useState } from 'react'
import { useTasks } from '../hooks/useTasks'

const TaskList: React.FC = () => {
  const { tasks, createTask } = useTasks()
  const [title, setTitle] = useState('')
  const [duration, setDuration] = useState(60)

  const handleAdd = () => {
    if (!title) return
    createTask({ title, duration_minutes: duration, priority: 'medium' })
    setTitle('')
  }

  return (
    <div className="p-4 overflow-auto flex-1">
      <h2 className="text-lg font-semibold mb-2">Tasks</h2>
      <div className="space-y-2">
        {tasks.map(t => (
          <div key={t.id} className="p-2 border rounded flex justify-between">
            <span>{t.title}</span>
            <span>{t.duration_minutes}m</span>
          </div>
        ))}
      </div>
      <div className="mt-4 flex space-x-2">
        <input
          className="flex-1 border rounded p-2"
          placeholder="New task"
          value={title}
          onChange={e => setTitle(e.target.value)}
        />
        <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={handleAdd}>
          Add
        </button>
      </div>
    </div>
  )
}

export default TaskList
