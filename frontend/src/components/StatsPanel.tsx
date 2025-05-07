import React from 'react'
import { useStats } from '../hooks/useStats'

const StatsPanel: React.FC = () => {
  const { stats } = useStats()
  if (!stats) return null

  return (
    <div className="p-4 border-t">
      <h2 className="text-lg font-semibold mb-2">Stats</h2>
      <div>Completion: {(stats.completion_rate * 100).toFixed(0)}%</div>
      <div>Missed tasks: {stats.missed_tasks}</div>
      <div>Streak: {stats.streak} days</div>
    </div>
  )
}

export default StatsPanel
