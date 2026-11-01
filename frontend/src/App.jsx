import React from 'react';
import Generator from './pages/Generator';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <nav className="bg-black/50 backdrop-blur-lg border-b border-purple-500/20">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg"></div>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              AI Music Studio
            </span>
          </div>
        </div>
      </nav>
      <Generator />
    </div>
  );
}

export default App;