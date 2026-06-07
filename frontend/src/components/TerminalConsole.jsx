import React, { useEffect, useState, useRef } from 'react';

const TerminalConsole = () => {
  const [logs, setLogs] = useState(['$ uvicorn api:app --host 0.0.0.0 --port 8000 --reload']);
  const endRef = useRef(null);

  useEffect(() => {
    let eventSource;
    let reconnectTimeout;

    const connect = () => {
      eventSource = new EventSource('http://127.0.0.1:8000/logs');
      
      eventSource.onopen = () => {
        setLogs((prev) => [...prev, "CONNECTED TO HTTP://127.0.0.1:8000/LOGS [SSE]..."]);
      };

      eventSource.onmessage = (event) => {
        setLogs((prevLogs) => [...prevLogs, event.data]);
      };

      eventSource.onerror = (error) => {
        setLogs((prev) => [...prev, "CONNECTION LOST. Retrying in 2 seconds..."]);
        eventSource.close();
        reconnectTimeout = setTimeout(connect, 2000);
      };
    };

    connect();

    return () => {
      clearTimeout(reconnectTimeout);
      if (eventSource) {
        eventSource.close();
      }
    };
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="terminal-console">
      {logs.map((log, i) => (
        <div key={i} className="log-line">{log}</div>
      ))}
      <div ref={endRef} />
    </div>
  );
};

export default TerminalConsole;
