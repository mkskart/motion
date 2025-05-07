import React from 'react'
import CalendarView from './components/CalendarView'
import TaskList from './components/TaskList'
import StatsPanel from './components/StatsPanel'
import LoginButton from './components/LoginButton'
import { useAuth } from './hooks/useAuth'

const App: React.FC = () => {
  const { user } = useAuth()
  if (!user) return <LoginButton />

  return (
    <div className="h-screen grid grid-cols-4">
      <div className="col-span-3 flex flex-col">
        <CalendarView />
      </div>
      <div className="col-span-1 flex flex-col border-l">
        <TaskList />
        <StatsPanel />
      </div>
    </div>
  )
}

export default App
