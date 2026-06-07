import React, { useState } from 'react';
import AudioRecorder from './components/AudioRecorder';
import TerminalConsole from './components/TerminalConsole';
import './index.css';

function App() {
  const [transcript, setTranscript] = useState('');

  return (
    <div className="app-wrapper">
      {/* LEFT SIDE: Input and Output */}
      <div className="left-panel">
        <div className="recorder-section">
          <div className="panel-header" style={{ position: 'absolute', top: 0, left: 0, right: 0 }}>
            <span>Input [MIC]</span>
          </div>
          <h1>STT Interface</h1>
          <AudioRecorder setTranscript={setTranscript} />
        </div>

        <div className="transcript-section">
          <div className="panel-header" style={{ position: 'sticky', top: '-1.5rem', margin: '-1.5rem -1.5rem 1.5rem', background: 'var(--term-bg)', zIndex: 1 }}>
            <span>Output [TRANSCRIPT]</span>
          </div>
          <div className="transcript-text">
            {transcript || "Awaiting audio input..."}
            <span className="cursor"></span>
          </div>
        </div>
      </div>

      {/* RIGHT SIDE: Terminal Streaming */}
      <div className="right-panel">
        <div className="panel-header">
          <span>Backend Server [uvicorn]</span>
        </div>
        <TerminalConsole />
      </div>
    </div>
  );
}

export default App;
