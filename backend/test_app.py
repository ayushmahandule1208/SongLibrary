# import pytest
# import json
# from app import create_app
# from models import db, Song
# from data_processor import DataProcessor


# @pytest.fixture
# def app():
#     """Create application for testing"""
#     app = create_app('testing')
    
#     with app.app_context():
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()


# @pytest.fixture
# def client(app):
#     """Create test client"""
#     return app.test_client()


# @pytest.fixture
# def sample_songs(app):
#     """Create sample songs for testing"""
#     with app.app_context():
#         songs = [
#             Song(
#                 index=0,
#                 id='test_id_1',
#                 title='Test Song 1',
#                 danceability=0.5,
#                 energy=0.7,
#                 tempo=120.0,
#                 duration_ms=200000,
#                 star_rating=0
#             ),
#             Song(
#                 index=1,
#                 id='test_id_2',
#                 title='Test Song 2',
#                 danceability=0.8,
#                 energy=0.9,
#                 tempo=140.0,
#                 duration_ms=180000,
#                 star_rating=3
#             ),
#             Song(
#                 index=2,
#                 id='test_id_3',
#                 title='Another Song',
#                 danceability=0.6,
#                 energy=0.5,
#                 tempo=100.0,
#                 duration_ms=220000,
#                 star_rating=5
#             )
#         ]
        
#         for song in songs:
#             db.session.add(song)
        
#         db.session.commit()
#         return songs


# class TestHealthCheck:
#     """Test health check endpoint"""
    
#     def test_index_endpoint(self, client):
#         """Test GET / endpoint"""
#         response = client.get('/')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert 'version' in data
#         assert 'endpoints' in data


# class TestGetAllSongs:
#     """Test GET /api/songs endpoint"""
    
#     def test_get_all_songs_empty(self, client):
#         """Test getting all songs when database is empty"""
#         response = client.get('/api/songs')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert len(data['data']) == 0
    
#     def test_get_all_songs_with_data(self, client, sample_songs):
#         """Test getting all songs with data"""
#         response = client.get('/api/songs')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert len(data['data']) == 3
#         assert 'pagination' in data
    
#     def test_pagination(self, client, sample_songs):
#         """Test pagination parameters"""
#         response = client.get('/api/songs?page=1&per_page=2')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert len(data['data']) == 2
#         assert data['pagination']['page'] == 1
#         assert data['pagination']['per_page'] == 2
#         assert data['pagination']['total_items'] == 3
#         assert data['pagination']['has_next'] == True
    
#     def test_sorting_asc(self, client, sample_songs):
#         """Test sorting in ascending order"""
#         response = client.get('/api/songs?sort_by=tempo&order=asc')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         tempos = [song['tempo'] for song in data['data']]
#         assert tempos == sorted(tempos)
    
#     def test_sorting_desc(self, client, sample_songs):
#         """Test sorting in descending order"""
#         response = client.get('/api/songs?sort_by=energy&order=desc')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         energies = [song['energy'] for song in data['data']]
#         assert energies == sorted(energies, reverse=True)
    
#     def test_invalid_page(self, client):
#         """Test invalid page number"""
#         response = client.get('/api/songs?page=0')
#         assert response.status_code == 400
    
#     def test_invalid_per_page(self, client):
#         """Test invalid per_page value"""
#         response = client.get('/api/songs?per_page=1000')
#         assert response.status_code == 400
    
#     def test_invalid_sort_column(self, client):
#         """Test invalid sort column"""
#         response = client.get('/api/songs?sort_by=invalid_column')
#         assert response.status_code == 400


# class TestSearchSongs:
#     """Test GET /api/songs/search endpoint"""
    
#     def test_search_exact_match(self, client, sample_songs):
#         """Test exact title match"""
#         response = client.get('/api/songs/search?title=Test Song 1&exact=true')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert len(data['data']) == 1
#         assert data['data'][0]['title'] == 'Test Song 1'
    
#     def test_search_partial_match(self, client, sample_songs):
#         """Test partial title match"""
#         response = client.get('/api/songs/search?title=Test')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert len(data['data']) == 2  # Should match "Test Song 1" and "Test Song 2"
    
#     def test_search_case_insensitive(self, client, sample_songs):
#         """Test case-insensitive search"""
#         response = client.get('/api/songs/search?title=test song')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert len(data['data']) >= 1
    
#     def test_search_no_results(self, client, sample_songs):
#         """Test search with no results"""
#         response = client.get('/api/songs/search?title=NonexistentSong')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert len(data['data']) == 0
    
#     def test_search_missing_title(self, client):
#         """Test search without title parameter"""
#         response = client.get('/api/songs/search')
#         assert response.status_code == 400


# class TestGetSongById:
#     """Test GET /api/songs/<song_id> endpoint"""
    
#     def test_get_existing_song(self, client, sample_songs):
#         """Test getting an existing song by ID"""
#         response = client.get('/api/songs/test_id_1')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert data['data']['id'] == 'test_id_1'
#         assert data['data']['title'] == 'Test Song 1'
    
#     def test_get_nonexistent_song(self, client):
#         """Test getting a non-existent song"""
#         response = client.get('/api/songs/nonexistent_id')
#         assert response.status_code == 404
        
#         data = json.loads(response.data)
#         assert data['status'] == 'error'


# class TestUpdateRating:
#     """Test PUT /api/songs/<song_id>/rating endpoint"""
    
#     def test_update_rating_success(self, client, sample_songs):
#         """Test successfully updating rating"""
#         response = client.put(
#             '/api/songs/test_id_1/rating',
#             json={'rating': 4},
#             content_type='application/json'
#         )
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert data['data']['star_rating'] == 4
    
#     def test_update_rating_invalid_value(self, client, sample_songs):
#         """Test updating rating with invalid value"""
#         response = client.put(
#             '/api/songs/test_id_1/rating',
#             json={'rating': 10},
#             content_type='application/json'
#         )
#         assert response.status_code == 400
    
#     def test_update_rating_missing_data(self, client, sample_songs):
#         """Test updating rating without rating data"""
#         response = client.put(
#             '/api/songs/test_id_1/rating',
#             json={},
#             content_type='application/json'
#         )
#         assert response.status_code == 400
    
#     def test_update_rating_nonexistent_song(self, client):
#         """Test updating rating for non-existent song"""
#         response = client.put(
#             '/api/songs/nonexistent_id/rating',
#             json={'rating': 3},
#             content_type='application/json'
#         )
#         assert response.status_code == 404


# class TestUploadData:
#     """Test POST /api/songs/upload endpoint"""
    
#     def test_upload_valid_data(self, client):
#         """Test uploading valid JSON data"""
#         json_data = {
#             "id": {"0": "upload_test_1", "1": "upload_test_2"},
#             "title": {"0": "Upload Song 1", "1": "Upload Song 2"},
#             "danceability": {"0": "0.5", "1": "0.7"},
#             "energy": {"0": "0.6", "1": "0.8"}
#         }
        
#         response = client.post(
#             '/api/songs/upload',
#             json=json_data,
#             content_type='application/json'
#         )
#         assert response.status_code == 201
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert data['inserted_count'] == 2
    
#     def test_upload_empty_data(self, client):
#         """Test uploading empty data"""
#         response = client.post(
#             '/api/songs/upload',
#             json={},
#             content_type='application/json'
#         )
#         assert response.status_code == 400
    
#     def test_upload_no_data(self, client):
#         """Test uploading without data"""
#         response = client.post('/api/songs/upload')
#         assert response.status_code == 400


# class TestStats:
#     """Test GET /api/stats endpoint"""
    
#     def test_get_stats_with_data(self, client, sample_songs):
#         """Test getting statistics with data"""
#         response = client.get('/api/stats')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['status'] == 'success'
#         assert data['data']['total_songs'] == 3
#         assert 'average_danceability' in data['data']
#         assert 'rating_distribution' in data['data']
    
#     def test_get_stats_empty(self, client):
#         """Test getting statistics with empty database"""
#         response = client.get('/api/stats')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data['data']['total_songs'] == 0


# class TestDataProcessor:
#     """Test DataProcessor class"""
    
#     def test_normalize_json(self):
#         """Test JSON normalization"""
#         json_data = {
#             "id": {"0": "test1", "1": "test2"},
#             "title": {"0": "Song1", "1": "Song2"},
#             "danceability": {"0": "0.5", "1": "0.7"}
#         }
        
#         result = DataProcessor.normalize_json(json_data)
        
#         assert len(result) == 2
#         assert result[0]['id'] == 'test1'
#         assert result[0]['title'] == 'Song1'
#         assert result[0]['danceability'] == 0.5
#         assert result[1]['index'] == 1
    
#     def test_normalize_empty_json(self):
#         """Test normalizing empty JSON"""
#         with pytest.raises(ValueError):
#             DataProcessor.normalize_json({})
    
#     def test_convert_value_int(self):
#         """Test integer conversion"""
#         result = DataProcessor._convert_value('duration_ms', '200000')
#         assert result == 200000
#         assert isinstance(result, int)
    
#     def test_convert_value_float(self):
#         """Test float conversion"""
#         result = DataProcessor._convert_value('danceability', '0.75')
#         assert result == 0.75
#         assert isinstance(result, float)
    
#     def test_convert_value_string(self):
#         """Test string conversion"""
#         result = DataProcessor._convert_value('title', 'Test Song')
#         assert result == 'Test Song'
#         assert isinstance(result, str)


# class TestSongModel:
#     """Test Song model"""
    
#     def test_song_to_dict(self, app):
#         """Test converting song to dictionary"""
#         with app.app_context():
#             song = Song(
#                 index=0,
#                 id='test_id',
#                 title='Test Song',
#                 danceability=0.5,
#                 star_rating=3
#             )
            
#             song_dict = song.to_dict()
            
#             assert song_dict['id'] == 'test_id'
#             assert song_dict['title'] == 'Test Song'
#             assert song_dict['danceability'] == 0.5
#             assert song_dict['star_rating'] == 3
    
#     def test_validate_rating_valid(self):
#         """Test valid rating validation"""
#         assert Song.validate_rating(3) == True
#         assert Song.validate_rating(0) == True
#         assert Song.validate_rating(5) == True
    
#     def test_validate_rating_invalid(self):
#         """Test invalid rating validation"""
#         with pytest.raises(ValueError):
#             Song.validate_rating(6)
        
#         with pytest.raises(ValueError):
#             Song.validate_rating(-1)
        
#         with pytest.raises(ValueError):
#             Song.validate_rating(3.5)


# class TestErrorHandlers:
#     """Test error handlers"""
    
#     def test_404_error(self, client):
#         """Test 404 error handler"""
#         response = client.get('/api/nonexistent')
#         assert response.status_code == 404
        
#         data = json.loads(response.data)
#         assert data['status'] == 'error'
    
#     def test_405_error(self, client):
#         """Test 405 error handler"""
#         response = client.post('/')  # GET-only endpoint
#         assert response.status_code == 405
        
#         data = json.loads(response.data)
#         assert data['status'] == 'error'


# if __name__ == '__main__':
#     pytest.main(['-v', '--cov=.', '--cov-report=html'])

