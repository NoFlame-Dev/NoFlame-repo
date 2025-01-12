import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Fire from "./Fire";

function App() {
  const [firePercentage, setFirePercentage] = useState(0)
  const HandleIncrease = () => {
    if (firePercentage < 100) {
      setFirePercentage(firePercentage + 10);
    }
  };

  const HandleDecrease = () => {
    if (firePercentage > 0) {
      setFirePercentage(firePercentage - 10);
    }
  };

  return (
    <div className='dashboard'>
      <header className='dashboard-header'>
        <h1>DASHBOARD</h1>
      </header>

      <div className="boxes">
        <div className="left-column"> 
          <div className="rounded-box">Temperature</div>
          <div className="rounded-box">Humidity</div>
          <div className="rounded-box">Wind Speed</div>
          <div className="rounded-box">Positive</div>
        </div>
       
        <div className="center-column">
          <div className="fire-percentage"> 
            {firePercentage > 0 && (
              <div 
                className="fire-container"
                style={{
                  transform: `scale(${firePercentage/100})`,
                }}
              >
                <Fire />
              </div>
            )}
            <div className="percentage-text">{firePercentage}%</div>
          </div>
          <div className="safety-list">Safety checklist</div>
        </div>

        <div className="right-column">
          <div className="fire-likely"> Fire is likely </div>
          <div className="map"> map </div>
        </div>
      </div>

      {/* Buttons to control fire intensity */}
      <div className="controls">
        <button onClick={HandleDecrease}>Decrease Fire</button>
        <button onClick={HandleIncrease}>Increase Fire</button>
      </div>
      
    </div>
  );
}

export default App
