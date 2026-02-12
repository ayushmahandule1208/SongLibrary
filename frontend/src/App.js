import React, { useMemo, useState, useEffect } from 'react';
import {
  BarChart3,
  Database,
  Search,
} from 'lucide-react';
import { Toaster, toast } from 'react-hot-toast';
import SearchBar from './components/SearchBar';
import SongTable from './components/SongTable';
import Pagination from './components/Pagination';
import CSVDownload from './components/CSVDownload';
import Charts from './components/Charts';
import { songsAPI } from './services/api';
import './App.css';

function App() {
  const [songs, setSongs] = useState([]);
  const [allSongs, setAllSongs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFetching, setIsFetching] = useState(false);
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);
  const [stats, setStats] = useState(null);
  const [activeTab, setActiveTab] = useState('table');
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [perPage] = useState(10);
  
  // Sorting state
  const [sortBy, setSortBy] = useState('index');
  const [sortOrder, setSortOrder] = useState('asc');

  // Fetch songs
  const fetchSongs = async (page = 1, sort = sortBy, order = sortOrder, opts = {}) => {
    const { showLoader = true } = opts;
    try {
      if (showLoader) setLoading(true);
      else setIsFetching(true);
      const response = await songsAPI.getAllSongs({
        page,
        per_page: perPage,
        sort_by: sort,
        order,
      });

      if (response.data.status === 'success') {
        setSongs(response.data.data);
        setCurrentPage(response.data.pagination.page);
        setTotalPages(response.data.pagination.total_pages);
        setTotalItems(response.data.pagination.total_items);
        setHasLoadedOnce(true);
      }
    } catch (error) {
      console.error('Error fetching songs:', error);
      toast.error('Failed to load songs');
    } finally {
      setLoading(false);
      setIsFetching(false);
    }
  };

  // Fetch all songs for CSV and charts
  const fetchAllSongs = async () => {
    try {
      let allSongsData = [];
      let currentPage = 1;
      let hasMore = true;
      const perPageLimit = 100;

      while (hasMore) {
        const response = await songsAPI.getAllSongs({
          page: currentPage,
          per_page: perPageLimit,
          sort_by: 'index',
          order: 'asc',
        });

        if (response.data.status === 'success') {
          allSongsData = [...allSongsData, ...response.data.data];
          const totalPages = response.data.pagination?.total_pages || 1;
          hasMore = currentPage < totalPages;
          currentPage++;
        } else {
          hasMore = false;
        }
      }

      setAllSongs(allSongsData);
    } catch (error) {
      console.error('Error fetching all songs:', error);
    }
  };

  // Fetch stats
  const fetchStats = async () => {
    try {
      const response = await songsAPI.getStats();
      if (response.data.status === 'success') {
        setStats(response.data.data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  useEffect(() => {
    fetchSongs();
    fetchAllSongs();
    fetchStats();
  }, []);

  // Handle search
  const handleSearch = async (title) => {
    try {
      setLoading(true);
      const response = await songsAPI.searchSongs(title, false);

      if (response.data.status === 'success') {
        setSongs(response.data.data);
        setTotalItems(response.data.count || 0);
        setTotalPages(1);
        setCurrentPage(1);
        
        if (response.data.count === 0) {
          toast.error('No songs found');
        } else {
          toast.success(`Found ${response.data.count} song(s)`);
        }
      }
    } catch (error) {
      console.error('Error searching:', error);
      toast.error('Search failed');
    } finally {
      setLoading(false);
    }
  };

  // Handle clear search
  const handleClearSearch = () => {
    fetchSongs(1, sortBy, sortOrder);
  };

  // Handle sort
  const handleSort = (column) => {
    const newOrder = sortBy === column && sortOrder === 'asc' ? 'desc' : 'asc';
    setSortBy(column);
    setSortOrder(newOrder);
    // Keep the table visible while we fetch the sorted page
    fetchSongs(currentPage, column, newOrder, { showLoader: false });
  };

  // Handle page change
  const handlePageChange = (page) => {
    fetchSongs(page, sortBy, sortOrder);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Handle rating update
  const handleRatingUpdate = async (songId, rating) => {
    try {
      const response = await songsAPI.updateRating(songId, rating);
      
      if (response.data.status === 'success') {
        // Update local state
        setSongs(prevSongs =>
          prevSongs.map(song =>
            song.id === songId ? { ...song, star_rating: rating } : song
          )
        );
        
        setAllSongs(prevSongs =>
          prevSongs.map(song =>
            song.id === songId ? { ...song, star_rating: rating } : song
          )
        );
        
        toast.success('Rating updated!', {
          duration: 2000,
        });
      }
    } catch (error) {
      console.error('Error updating rating:', error);
      toast.error('Failed to update rating');
    }
  };

  const topRated = useMemo(() => {
    const src = Array.isArray(allSongs) && allSongs.length ? allSongs : songs;
    return [...src]
      .filter((s) => (s.star_rating || 0) > 0)
      .sort((a, b) => (b.star_rating || 0) - (a.star_rating || 0))
      .slice(0, 5);
  }, [allSongs, songs]);

  return (
    <div className="App">
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: 'rgba(40, 40, 40, 0.95)',
            color: '#fff',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(20px)',
          },
          success: {
            iconTheme: {
              primary: '#1DB954',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#ff6b6b',
              secondary: '#fff',
            },
          },
        }}
      />

      <div className="app-shell">
        {/* Main */}
        <main className="main">
          <div className="topbar">
            <div className="topbar-actions">
              <div className="pill glass-card">Now Playing</div>
              <div className="avatar glass-card" aria-label="Profile" />
            </div>
          </div>

          <header className="hero">
            <div className="hero-title">Playlist Dashboard</div>
            <div className="hero-subtitle">Modern analytics for your music collection</div>
          </header>

          <div className="tabs-container">
            <button
              className={`tab-button ${activeTab === 'table' ? 'active' : ''}`}
              onClick={() => setActiveTab('table')}
            >
              <Database size={18} />
              <span>Table</span>
            </button>
            <button
              className={`tab-button ${activeTab === 'charts' ? 'active' : ''}`}
              onClick={() => setActiveTab('charts')}
            >
              <BarChart3 size={18} />
              <span>Charts</span>
            </button>
          </div>

          {/* Table Tab */}
          {activeTab === 'table' && (
            <>
              <div className="section-row">
                <SearchBar onSearch={handleSearch} onClear={handleClearSearch} />
                <CSVDownload data={allSongs} filename="playlist_songs.csv" />
              </div>

              <div className="table-container">
                {loading && !hasLoadedOnce ? (
                  <div className="loading-container glass-card">
                    <div className="spinner"></div>
                    <p className="loading-text">Loading your music...</p>
                  </div>
                ) : (
                  <>
                    {isFetching && (
                      <div className="table-fetching" aria-live="polite">
                        <div className="spinner spinner--sm" />
                        <span>Updating…</span>
                      </div>
                    )}
                    <SongTable
                      songs={songs}
                      onSort={handleSort}
                      sortBy={sortBy}
                      sortOrder={sortOrder}
                      onRateUpdate={handleRatingUpdate}
                    />

                    {totalPages > 1 && (
                      <Pagination
                        currentPage={currentPage}
                        totalPages={totalPages}
                        totalItems={totalItems}
                        perPage={perPage}
                        onPageChange={handlePageChange}
                      />
                    )}
                  </>
                )}
              </div>
            </>
          )}

          {/* Charts Tab */}
          {activeTab === 'charts' && (
            <div className="charts-section">
              {allSongs.length > 0 ? (
                <Charts songs={allSongs} />
              ) : (
                <div className="loading-container glass-card">
                  <div className="spinner"></div>
                  <p className="loading-text">Loading charts...</p>
                </div>
              )}
            </div>
          )}
        </main>

        {/* Right Rail */}
        <aside className="right-rail">
          {stats && (
            <div className="rail-card glass-card">
              <div className="rail-title">Stats</div>
              <div className="rail-stats">
                <div className="rail-stat">
                  <div className="rail-stat-label">Songs</div>
                  <div className="rail-stat-value">{stats.total_songs}</div>
                </div>
                <div className="rail-stat">
                  <div className="rail-stat-label">Avg Dance</div>
                  <div className="rail-stat-value">{(stats.average_danceability || 0).toFixed(2)}</div>
                </div>
                <div className="rail-stat">
                  <div className="rail-stat-label">Avg Energy</div>
                  <div className="rail-stat-value">{(stats.average_energy || 0).toFixed(2)}</div>
                </div>
              </div>
            </div>
          )}

          <div className="rail-card glass-card">
            <div className="rail-title">Top Rated</div>
            {topRated.length ? (
              <div className="rail-list">
                {topRated.map((s) => (
                  <div className="rail-item" key={s.id}>
                    <div className="rail-item-main">
                      <div className="rail-item-title">{s.title}</div>
                      <div className="rail-item-sub">ID: {s.id}</div>
                    </div>
                    <div className="rail-item-meta">{s.star_rating}/5</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="rail-empty">Rate a few songs to populate this list.</div>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;