import React, { useState } from 'react';
import { ChevronUp, ChevronDown, Music } from 'lucide-react';
import StarRating from './StarRating';
import { formatDuration, formatNumber } from '../utils/csvExport';
import './SongTable.css';

const SongTable = ({ songs, onSort, sortBy, sortOrder, onRateUpdate }) => {
  const [hoveredRow, setHoveredRow] = useState(null);
  const [selectedSong, setSelectedSong] = useState(null);

  const columns = [
    { key: 'index', label: '', width: '60px' },
    { key: 'title', label: 'Title', width: 'minmax(200px, 1fr)' },
    { key: 'danceability', label: 'Danceability', width: '150px' },
    { key: 'energy', label: 'Energy', width: '130px' },
    { key: 'tempo', label: 'Tempo', width: '100px' },
    { key: 'duration_ms', label: 'Duration', width: '120px' },
    { key: 'star_rating', label: 'Rating', width: '140px' },
  ];

  const getSortIcon = (columnKey) => {
    if (sortBy !== columnKey) return null;
    return sortOrder === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />;
  };

  const getProgressBarColor = (value, type) => {
    if (type === 'danceability') {
      if (value > 0.7) return '#1DB954';
      if (value > 0.4) return '#FFD700';
      return '#ff6b6b';
    }
    if (type === 'energy') {
      if (value > 0.7) return '#f093fb';
      if (value > 0.4) return '#4facfe';
      return '#667eea';
    }
    return '#1DB954';
  };

  return (
    <div className="song-table-container">
      <div className="table-wrapper glass-card">
        <div className="table-grid" style={{
          gridTemplateColumns: columns.map(col => col.width).join(' ')
        }}>
          <div className="table-header-row">
            {columns.map((column) => (
              <div
                key={column.key}
                className={`table-header-cell ${column.key === sortBy ? 'active' : ''}`}
                onClick={() => column.key !== 'star_rating' && onSort(column.key)}
              >
                <div className="header-content">
                  <span>{column.label}</span>
                  {column.key !== 'star_rating' && getSortIcon(column.key)}
                </div>
              </div>
            ))}
          </div>

          {songs.map((song, index) => (
            <React.Fragment key={song.id}>
              <div
                className={`table-row ${hoveredRow === index ? 'hovered' : ''}`}
                onMouseEnter={() => setHoveredRow(index)}
                onMouseLeave={() => setHoveredRow(null)}
                onClick={() => setSelectedSong(song)}
              >
                <div className="table-cell index-cell">
                  {hoveredRow === index ? (
                    <Music size={18} className="play-icon" />
                  ) : (
                    <span>{song.index + 1}</span>
                  )}
                </div>

                <div className="table-cell title-cell">
                  <div className="song-info">
                    <div className="song-cover">
                      <Music size={16} />
                    </div>
                    <div className="song-details">
                      <div className="song-title">{song.title}</div>
                      <div className="song-id">{song.id}</div>
                    </div>
                  </div>
                </div>

                <div className="table-cell">
                  <div className="progress-cell">
                    <div className="progress-bar-container">
                      <div
                        className="progress-bar"
                        style={{
                          width: `${(song.danceability || 0) * 100}%`,
                          background: getProgressBarColor(song.danceability || 0, 'danceability')
                        }}
                      />
                    </div>
                    <span className="progress-value">{formatNumber(song.danceability)}</span>
                  </div>
                </div>

                <div className="table-cell">
                  <div className="progress-cell">
                    <div className="progress-bar-container">
                      <div
                        className="progress-bar"
                        style={{
                          width: `${(song.energy || 0) * 100}%`,
                          background: getProgressBarColor(song.energy || 0, 'energy')
                        }}
                      />
                    </div>
                    <span className="progress-value">{formatNumber(song.energy)}</span>
                  </div>
                </div>

                <div className="table-cell">
                  <span className="tempo-value">{song.tempo ? Math.round(song.tempo) : '-'}</span>
                  <span className="tempo-unit">BPM</span>
                </div>

                <div className="table-cell">
                  {formatDuration(song.duration_ms)}
                </div>

                <div className="table-cell rating-cell">
                  <StarRating
                    rating={song.star_rating || 0}
                    songId={song.id}
                    onRate={onRateUpdate}
                  />
                </div>
              </div>
            </React.Fragment>
          ))}
        </div>

        {songs.length === 0 && (
          <div className="empty-table">
            <Music size={64} className="empty-icon" />
            <p className="empty-text">No songs found</p>
            <p className="empty-subtext">Try adjusting your search or filters</p>
          </div>
        )}
      </div>

      {selectedSong && (
        <div
          className="song-detail-overlay"
          onClick={() => setSelectedSong(null)}
        >
          <div
            className="song-detail-modal glass-card"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              type="button"
              className="song-detail-close"
              onClick={() => setSelectedSong(null)}
            >
              Close
            </button>
            <div className="song-detail-header">
              <div className="song-detail-cover">
                <Music size={28} />
              </div>
              <div className="song-detail-meta">
                <div className="song-detail-title">{selectedSong.title}</div>
                <div className="song-detail-id">ID: {selectedSong.id}</div>
              </div>
            </div>

            <div className="song-detail-body">
              <div className="song-detail-row">
                <span className="song-detail-label">Danceability</span>
                <span className="song-detail-value">
                  {formatNumber(selectedSong.danceability)}
                </span>
              </div>
              <div className="song-detail-row">
                <span className="song-detail-label">Energy</span>
                <span className="song-detail-value">
                  {formatNumber(selectedSong.energy)}
                </span>
              </div>
              <div className="song-detail-row">
                <span className="song-detail-label">Tempo</span>
                <span className="song-detail-value">
                  {selectedSong.tempo ? Math.round(selectedSong.tempo) : '-'} BPM
                </span>
              </div>
              <div className="song-detail-row">
                <span className="song-detail-label">Duration</span>
                <span className="song-detail-value">
                  {formatDuration(selectedSong.duration_ms)}
                </span>
              </div>
              <div className="song-detail-row">
                <span className="song-detail-label">Rating</span>
                <span className="song-detail-value">
                  {selectedSong.star_rating || 0} / 5
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SongTable;