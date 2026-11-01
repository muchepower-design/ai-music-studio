import React, { useEffect, useRef, useState } from 'react';

export default function Waveform({ audioUrl, taskId }) {
  const canvasRef = useRef(null);
  const [waveformData, setWaveformData] = useState(null);

  useEffect(() => {
    if (!taskId) return;
    fetch(`http://localhost:8000/api/waveform/${taskId}`)
      .then(res => res.json())
      .then(data => setWaveformData(data.waveform))
      .catch(console.error);
  }, [taskId]);

  useEffect(() => {
    if (!waveformData || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = '#a855f7';
    const barWidth = width / waveformData.length;
    let x = 0;
    for (let amp of waveformData) {
      const barHeight = (Math.abs(amp) * height) / 2;
      ctx.fillRect(x, (height - barHeight) / 2, barWidth - 1, barHeight);
      x += barWidth;
    }
  }, [waveformData]);

  return (
    <div className="mt-4">
      <canvas ref={canvasRef} width={600} height={100} className="w-full rounded-lg bg-black/30" />
      <audio controls className="w-full mt-4" src={audioUrl} />
    </div>
  );
}