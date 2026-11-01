import React, { useState } from 'react';
import axios from 'axios';
import Waveform from '../components/Waveform';

const genres = ['country', 'hip-hop', 'raggae', 'rhumba', 'rnb', 'afrobeats'];

export default function Generator() {
  const [prompt, setPrompt] = useState('');
  const [genre, setGenre] = useState('hip-hop');
  const [duration, setDuration] = useState(30);
  const [includeVocals, setIncludeVocals] = useState(false);
  const [lyrics, setLyrics] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const res = await axios.post('http://localhost:8000/api/generate', {
        prompt,
        genre,
        duration,
        include_vocals: includeVocals,
        lyrics: includeVocals ? lyrics : null
      });
      setTaskId(res.data.task_id);
      pollStatus(res.data.task_id);
    } catch (err) {
      console.error(err);
      setIsGenerating(false);
    }
  };

  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`http://localhost:8000/api/status/${id}`);
        if (res.data.status === 'completed') {
          clearInterval(interval);
          setIsGenerating(false);
          setAudioUrl(`http://localhost:8000${res.data.download_url}`);
        }
      } catch (err) {
        console.error(err);
      }
    }, 2000);
  };

  return (
    <div className="container mx-auto px-6 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-5xl font-bold text-center mb-4 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          Create Your Music
        </h1>
        <p className="text-gray-400 text-center mb-12">
          Describe your sound and let AI compose it
        </p>

        <div className="bg-black/30 backdrop-blur-lg rounded-2xl p-8 border border-purple-500/20">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Musical Description
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="E.g., Upbeat country song with acoustic guitar, harmonica solo..."
                className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 text-white"
                rows="3"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Genre</label>
              <div className="grid grid-cols-3 gap-3">
                {genres.map((g) => (
                  <button
                    key={g}
                    onClick={() => setGenre(g)}
                    className={`px-4 py-2 rounded-lg capitalize transition ${
                      genre === g
                        ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                        : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    {g}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Duration: {duration} sec
              </label>
              <input
                type="range"
                min="10"
                max="60"
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={includeVocals}
                  onChange={(e) => setIncludeVocals(e.target.checked)}
                  className="w-5 h-5 rounded border-gray-700 bg-gray-800 text-purple-500"
                />
                <span className="text-gray-300">Include AI vocals</span>
              </label>
            </div>

            {includeVocals && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Lyrics</label>
                <textarea
                  value={lyrics}
                  onChange={(e) => setLyrics(e.target.value)}
                  placeholder="Enter lyrics here..."
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                  rows="4"
                />
              </div>
            )}

            <button
              onClick={handleGenerate}
              disabled={isGenerating || !prompt}
              className="w-full py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:shadow-lg transition disabled:opacity-50"
            >
              {isGenerating ? 'Generating...' : 'Generate Track'}
            </button>
          </div>
        </div>

        {audioUrl && (
  <div className="mt-8 bg-black/30 backdrop-blur-lg rounded-2xl p-6">
    <h3 className="text-xl font-semibold text-white mb-4">Your Track</h3>
    <Waveform audioUrl={audioUrl} taskId={taskId} />
    <div className="mt-4 text-center">
      <a href={audioUrl} download className="px-6 py-2 bg-green-600 rounded-lg text-white hover:bg-green-700">
        Download MP3
      </a>
    </div>
  </div>
)}
      </div>
    </div>
  );
}