import React from 'react';
import {
  ScatterChart,
  Scatter,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import './Charts.css';

const Charts = ({ songs }) => {
  const danceabilityData = songs.map((song, index) => ({
    index: index + 1,
    danceability: song.danceability,
    title: song.title,
  }));

  const durationBins = [0, 120000, 180000, 240000, 300000, 360000, 500000];
  const durationLabels = ['0-2m', '2-3m', '3-4m', '4-5m', '5-6m', '6m+'];
  const durationData = durationLabels.map((label, index) => {
    const min = durationBins[index];
    const max = durationBins[index + 1] || Infinity;
    const count = songs.filter(s => s.duration_ms >= min && s.duration_ms < max).length;
    return { label, count };
  });

  const acousticsData = songs
    .filter(song => song.acousticness != null)
    .slice(0, 20)
    .map((song, index) => ({
      name: song.title.substring(0, 12) + (song.title.length > 12 ? '...' : ''),
      value: song.acousticness || 0,
    }));

  const tempoData = songs
    .slice(0, 20)
    .map((song) => ({
      name: song.title.substring(0, 12) + (song.title.length > 12 ? '...' : ''),
      value: Math.round(song.tempo),
    }));

  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload || !payload.length) return null;

    const entry = payload[0];
    const title = entry.payload.title || entry.payload.name;
    const value =
      typeof entry.value === 'number' ? entry.value.toFixed(3) : entry.value;

    return (
      <div className="custom-tooltip">
        <p className="tooltip-label">{title}</p>
        <p className="tooltip-value">Danceability: {value}</p>
      </div>
    );
  };

  const COLORS = ['#4facfe', '#00f2fe', '#43e97b', '#38f9d7', '#667eea', '#f093fb'];

  return (
    <div className="charts-container">
      <div className="charts-grid">
        <div className="chart-card glass-card">
          <h3 className="chart-title">Danceability Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid
                strokeDasharray="2 4"
                stroke="rgba(255,255,255,0.08)"
              />
              <XAxis
                type="number"
                dataKey="index"
                name="Song"
                stroke="#b3b3b3"
                tick={{ fill: '#b3b3b3' }}
              />
              <YAxis
                type="number"
                dataKey="danceability"
                name="Danceability"
                stroke="#888888"
                tick={{ fill: '#b3b3b3', fontSize: 11 }}
                domain={[0, 1]}
              />
              <Tooltip
                content={<CustomTooltip />}
                cursor={{ stroke: 'rgba(255,255,255,0.25)', strokeWidth: 1 }}
                wrapperStyle={{ outline: 'none' }}
              />
              <Scatter data={danceabilityData} fill="#4facfe">
                {danceabilityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card glass-card">
          <h3 className="chart-title">Song Duration Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={durationData} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid
                strokeDasharray="2 4"
                stroke="rgba(255,255,255,0.07)"
                vertical={false}
              />
              <XAxis dataKey="label" stroke="#888888" tick={{ fill: '#b3b3b3', fontSize: 11 }} />
              <YAxis stroke="#888888" tick={{ fill: '#b3b3b3', fontSize: 11 }} />
              <Tooltip
                contentStyle={{
                  background: 'rgba(16, 16, 16, 0.98)',
                  border: '1px solid rgba(255,255,255,0.12)',
                  borderRadius: '10px',
                  color: 'white',
                  boxShadow: '0 18px 45px rgba(0, 0, 0, 0.7)',
                }}
                labelStyle={{ color: '#ffffff' }}
                itemStyle={{ color: '#ffffff' }}
                cursor={{ fill: 'rgba(0,0,0,0.35)' }}
                wrapperStyle={{ outline: 'none' }}
              />
              <Bar dataKey="count" radius={[10, 10, 0, 0]}>
                {durationData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card glass-card">
          <h3 className="chart-title">Acousticness (Top 20 Songs)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={acousticsData}
              layout="vertical"
              margin={{ top: 20, right: 20, bottom: 20, left: 80 }}
            >
              <CartesianGrid
                strokeDasharray="2 4"
                stroke="rgba(255,255,255,0.07)"
                vertical={false}
              />
              <XAxis type="number" stroke="#888888" tick={{ fill: '#b3b3b3', fontSize: 11 }} domain={[0, 1]} />
              <YAxis
                type="category"
                dataKey="name"
                stroke="#888888"
                tick={{ fill: '#b3b3b3', fontSize: 11 }}
                width={110}
              />
              <Tooltip
                contentStyle={{
                  background: 'rgba(16, 16, 16, 0.98)',
                  border: '1px solid rgba(255,255,255,0.12)',
                  borderRadius: '10px',
                  color: 'white',
                  boxShadow: '0 18px 45px rgba(0, 0, 0, 0.7)',
                }}
                labelStyle={{ color: '#ffffff' }}
                itemStyle={{ color: '#ffffff' }}
                cursor={{ fill: 'rgba(0,0,0,0.35)' }}
                wrapperStyle={{ outline: 'none' }}
              />
              <Bar dataKey="value" fill="#667eea" radius={[0, 10, 10, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card glass-card">
          <h3 className="chart-title">Tempo (Top 20 Songs)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={tempoData}
              layout="vertical"
              margin={{ top: 20, right: 20, bottom: 20, left: 80 }}
            >
              <CartesianGrid
                strokeDasharray="2 4"
                stroke="rgba(255,255,255,0.07)"
                vertical={false}
              />
              <XAxis type="number" stroke="#888888" tick={{ fill: '#b3b3b3', fontSize: 11 }} />
              <YAxis
                type="category"
                dataKey="name"
                stroke="#888888"
                tick={{ fill: '#b3b3b3', fontSize: 11 }}
                width={110}
              />
              <Tooltip
                contentStyle={{
                  background: 'rgba(16, 16, 16, 0.98)',
                  border: '1px solid rgba(255,255,255,0.12)',
                  borderRadius: '10px',
                  color: 'white',
                  boxShadow: '0 18px 45px rgba(0, 0, 0, 0.7)',
                }}
                labelStyle={{ color: '#ffffff' }}
                itemStyle={{ color: '#ffffff' }}
                cursor={{ fill: 'rgba(0,0,0,0.35)' }}
                wrapperStyle={{ outline: 'none' }}
              />
              <Bar dataKey="value" fill="#f093fb" radius={[0, 10, 10, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Charts;