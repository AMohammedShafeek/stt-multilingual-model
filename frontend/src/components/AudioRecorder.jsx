import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, Pause, Upload } from 'lucide-react';
import axios from 'axios';
import WaveSurfer from 'wavesurfer.js';

const AudioRecorder = ({ setTranscript }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [modelSize, setModelSize] = useState('medium');
  const [targetLanguage, setTargetLanguage] = useState('auto');
  
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const waveformRef = useRef(null);
  const wavesurfer = useRef(null);
  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioBlob(file);
      setAudioUrl(URL.createObjectURL(file));
      setTranscript('');
    }
  };

  useEffect(() => {
    if (audioUrl && waveformRef.current) {
      wavesurfer.current = WaveSurfer.create({
        container: waveformRef.current,
        waveColor: '#555555',
        progressColor: '#ffffff',
        cursorColor: '#ffffff',
        barWidth: 4,
        barGap: 3,
        barRadius: 0,
        height: 60,
        url: audioUrl,
      });

      wavesurfer.current.on('play', () => setIsPlaying(true));
      wavesurfer.current.on('pause', () => setIsPlaying(false));
      wavesurfer.current.on('finish', () => setIsPlaying(false));

      return () => {
        if (wavesurfer.current) {
          wavesurfer.current.destroy();
        }
      };
    }
  }, [audioUrl]);

  const togglePlayback = () => {
    if (wavesurfer.current) {
      wavesurfer.current.playPause();
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
        setAudioBlob(blob);
        setAudioUrl(URL.createObjectURL(blob));
        chunksRef.current = [];
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setTranscript('');
    } catch (err) {
      console.error(err);
      alert("Microphone access required.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const resetRecording = () => {
    setAudioUrl(null);
    setAudioBlob(null);
    setTranscript('');
  };

  const submitAudio = async () => {
    if (!audioBlob) return;
    setIsSubmitting(true);
    setTranscript("PROCESSING DATA...");
    
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    formData.append('model_size', modelSize);
    formData.append('target_language', targetLanguage);

    try {
      const response = await axios.post('http://localhost:8000/transcribe', formData);
      setTranscript(response.data.transcript || `Error: ${response.data.error}`);
    } catch (error) {
      setTranscript("CONNECTION ERROR: Failed to reach backend.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', width: '100%', justifyContent: 'center' }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
          <label style={{ marginBottom: '0.25rem', color: 'var(--term-dim)', fontSize: '0.8rem' }}>MODEL</label>
          <select 
            className="btn" 
            value={modelSize} 
            onChange={(e) => setModelSize(e.target.value)}
            disabled={isSubmitting}
            style={{ width: '120px' }}
          >
            <option value="tiny">TINY</option>
            <option value="base">BASE</option>
            <option value="small">SMALL</option>
            <option value="medium">MEDIUM</option>
            <option value="large-v2">LARGE-V2</option>
          </select>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
          <label style={{ marginBottom: '0.25rem', color: 'var(--term-dim)', fontSize: '0.8rem' }}>LANGUAGE</label>
          <select 
            className="btn" 
            value={targetLanguage} 
            onChange={(e) => setTargetLanguage(e.target.value)}
            disabled={isSubmitting}
            style={{ width: '150px' }}
          >
            <option value="auto">AUTO-DETECT</option>
            <option value="ta">TAMIL (TA)</option>
            <option value="en">ENGLISH (EN)</option>
            <option value="hi">HINDI (HI)</option>
          </select>
        </div>
      </div>

      {!audioUrl ? (
        <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <button
              className={`record-btn ${isRecording ? 'recording' : ''}`}
              onClick={isRecording ? stopRecording : startRecording}
            >
              {isRecording ? <Square /> : <Mic />}
            </button>
            <p>{isRecording ? "[REC] RECORDING..." : "RECORD"}</p>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <button
              className="record-btn"
              onClick={() => fileInputRef.current.click()}
              disabled={isRecording}
            >
              <Upload />
            </button>
            <p>UPLOAD FILE</p>
            <input 
              type="file" 
              accept="audio/*" 
              style={{ display: 'none' }} 
              ref={fileInputRef}
              onChange={handleFileUpload}
            />
          </div>
        </div>
      ) : (
        <>
          <div style={{ width: '100%', maxWidth: '400px', marginBottom: '1.5rem', border: '1px solid var(--term-border)', padding: '1rem', backgroundColor: 'var(--term-bg)' }}>
            <div ref={waveformRef} style={{ marginBottom: '1rem', cursor: 'pointer' }}></div>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
              <button className="btn" onClick={togglePlayback} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                {isPlaying ? 'PAUSE' : 'PLAY'}
              </button>
            </div>
          </div>
          <div className="action-buttons">
            <button className="btn" onClick={resetRecording} disabled={isSubmitting}>
              [R] RE-RECORD
            </button>
            <button className="btn" onClick={submitAudio} disabled={isSubmitting}>
              [S] SUBMIT
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default AudioRecorder;
