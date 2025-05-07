import React from 'react'
import { Calendar, dateFnsLocalizer } from 'react-big-calendar'
import { format, parse, startOfWeek, getDay } from 'date-fns'
import enUS from 'date-fns/locale/en-US'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import { useTasks } from '../hooks/useTasks'

const locales = { 'en-US': enUS }
const localizer = dateFnsLocalizer({ format, parse, startOfWeek, getDay, locales })

const CalendarView: React.FC = () => {
  const { tasks } = useTasks()
  const events = tasks.map(t => ({
    id: t.id,
    title: t.title,
    start: new Date(t.scheduled_start!),
    end: new Date(t.scheduled_end!),
    allDay: false,
    resource: t,
  }))

  return (
    <Calendar
      localizer={localizer}
      events={events}
      defaultView="week"
      style={{ height: '100%' }}
      eventPropGetter={(event) => {
        const priority = event.resource.priority
        const colors: Record<string, string> = {
          high: 'bg-red-500',
          medium: 'bg-yellow-500',
          low: 'bg-green-500',
        }
        return { className: `text-white ${colors[priority]}` }
      }}
      tooltipAccessor={(event) => event.resource.description}
    />
  )
}

export default CalendarView
