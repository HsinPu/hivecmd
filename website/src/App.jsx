import React, { useState, useEffect } from 'react'

function App() {
  const [teams, setTeams] = useState([])
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [teamState, setTeamState] = useState({ agents: [], tasks: [] })

  useEffect(() => {
    fetch('/api/teams')
      .then(r => r.json())
      .then(setTeams)
  }, [])

  useEffect(() => {
    if (selectedTeam) {
      fetch(`/api/team/${selectedTeam}`)
        .then(r => r.json())
        .then(setTeamState)
    }
  }, [selectedTeam])

  return (
    <>
      <header className="header">
        <h1>🐝 HiveCmd</h1>
        <div className="status">
          <span><span className="status-dot"></span> Connected</span>
        </div>
      </header>
      <div className="container">
        <div className="grid">
          <div className="card">
            <h2>Teams</h2>
            <ul className="agent-list">
              {teams.map(t => (
                <li key={t} className="agent-item" onClick={() => setSelectedTeam(t)} style={{cursor:'pointer'}}>
                  <span className="agent-name">{t}</span>
                  <span>→</span>
                </li>
              ))}
              {teams.length === 0 && <li style={{color:'#8b949e'}}>No teams</li>}
            </ul>
          </div>
          <div className="card">
            <h2>Agents ({teamState.agents?.length || 0})</h2>
            <ul className="agent-list">
              {teamState.agents?.map(a => (
                <li key={a.name} className="agent-item">
                  <span className="agent-name">{a.name}</span>
                  <span className={`agent-status ${a.status}`}>{a.status}</span>
                </li>
              ))}
              {(!teamState.agents || teamState.agents.length === 0) && <li style={{color:'#8b949e'}}>No agents</li>}
            </ul>
          </div>
          <div className="card">
            <h2>Tasks ({teamState.tasks?.length || 0})</h2>
            <ul className="task-list">
              {teamState.tasks?.map(t => (
                <li key={t.id} className="task-item">
                  <span className="task-id">{t.id}</span>
                  <span className="task-desc">{t.description?.slice(0, 20)}</span>
                  <span className={`task-status ${t.status}`}>{t.status}</span>
                </li>
              ))}
              {(!teamState.tasks || teamState.tasks.length === 0) && <li style={{color:'#8b949e'}}>No tasks</li>}
            </ul>
          </div>
        </div>
      </div>
    </>
  )
}

export default App
