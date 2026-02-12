import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

jest.mock('./services/api', () => {
  const mockSongs = [
    {
      index: 0,
      id: 'song_1',
      title: 'Song One',
      danceability: 0.5,
      energy: 0.7,
      tempo: 120,
      duration_ms: 200000,
      star_rating: 3,
    },
    {
      index: 1,
      id: 'song_2',
      title: 'Song Two',
      danceability: 0.8,
      energy: 0.9,
      tempo: 130,
      duration_ms: 180000,
      star_rating: 4,
    },
  ];

  const paginatedResponse = {
    data: {
      status: 'success',
      data: mockSongs,
      pagination: {
        page: 1,
        per_page: 10,
        total_pages: 1,
        total_items: mockSongs.length,
        has_next: false,
        has_prev: false,
      },
    },
  };

  const statsResponse = {
    data: {
      status: 'success',
      data: {
        total_songs: mockSongs.length,
        average_danceability: 0.65,
        average_energy: 0.8,
        average_tempo: 125,
        average_duration_ms: 190000,
        min_duration_ms: 180000,
        max_duration_ms: 200000,
        rating_distribution: { '3': 1, '4': 1 },
      },
    },
  };

  return {
    __esModule: true,
    songsAPI: {
      getAllSongs: jest.fn(() => Promise.resolve(paginatedResponse)),
      getStats: jest.fn(() => Promise.resolve(statsResponse)),
      searchSongs: jest.fn(() => Promise.resolve({
        data: {
          status: 'success',
          data: [mockSongs[0]],
          count: 1,
        },
      })),
      updateRating: jest.fn(() => Promise.resolve({
        data: {
          status: 'success',
        },
      })),
    },
  };
});

describe('App', () => {
  test('loads and renders songs in the table view', async () => {
    render(<App />);

    expect(await screen.findByText('Song One')).toBeInTheDocument();
    expect(screen.getByText('Playlist Dashboard')).toBeInTheDocument();
    expect(screen.getByText(/Showing 1-2 of 2 songs/i)).toBeInTheDocument();
  });

  test('switches to charts tab and shows charts', async () => {
    render(<App />);

    // Wait for initial data so tabs content is ready
    await screen.findByText('Song One');

    fireEvent.click(screen.getByRole('button', { name: /charts/i }));

    expect(
      await screen.findByText(/Danceability Distribution/i)
    ).toBeInTheDocument();
  });

  test('performs a search when submitting from the search bar', async () => {
    const { songsAPI } = await import('./services/api');

    render(<App />);

    await screen.findByText('Song One');

    const input = screen.getByPlaceholderText(/Search songs by title/i);
    fireEvent.change(input, { target: { value: 'Song One' } });
    fireEvent.submit(input.closest('form'));

    await waitFor(() => {
      expect(songsAPI.searchSongs).toHaveBeenCalledWith('Song One', false);
    });
  });

  test('updates rating when a star is clicked', async () => {
    const { songsAPI } = await import('./services/api');

    render(<App />);

    await screen.findByText('Song One');

    const starButton = await screen.findByRole('button', {
      name: /Rate 5 out of 5 stars/i,
    });

    fireEvent.click(starButton);

    await waitFor(() => {
      expect(songsAPI.updateRating).toHaveBeenCalled();
    });
  });
});
