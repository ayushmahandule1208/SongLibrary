import json
import logging
from typing import Dict, List, Any
from models import db, Song

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and normalize JSON song data"""
    
    @staticmethod
    def normalize_json(json_data: Dict[str, Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Normalize JSON data from key-value pairs to list of records.
        
        Input format:
        {
            "id": {"0": "abc", "1": "def"},
            "title": {"0": "Song1", "1": "Song2"}
        }
        
        Output format:
        [
            {"index": 0, "id": "abc", "title": "Song1"},
            {"index": 1, "id": "def", "title": "Song2"}
        ]
        """
        if not json_data:
            raise ValueError("JSON data is empty")
        
        # Get all keys (column names)
        columns = list(json_data.keys())
        
        if not columns:
            raise ValueError("No columns found in JSON data")
        
        # Get number of records from first column
        first_column = columns[0]
        num_records = len(json_data[first_column])
        
        logger.info(f"Processing {num_records} records with {len(columns)} columns")
        
        # Normalize data
        normalized_data = []
        
        for i in range(num_records):
            record = {}
            key = str(i)
            
            for column in columns:
                if key in json_data[column]:
                    value = json_data[column][key]
                    
                    # Convert data types appropriately
                    record[column] = DataProcessor._convert_value(column, value)
                else:
                    record[column] = None
            
            # Add index
            record['index'] = i
            normalized_data.append(record)
        
        logger.info(f"Successfully normalized {len(normalized_data)} records")
        return normalized_data
    
    @staticmethod
    def _convert_value(column: str, value: str) -> Any:
        """Convert string values to appropriate data types"""
        if value == '' or value is None:
            return None
        
        # Integer columns
        if column in ['index', 'key', 'mode', 'time_signature', 'duration_ms', 
                      'num_bars', 'num_sections', 'num_segments', 'class', 'star_rating']:
            try:
                return int(value)
            except (ValueError, TypeError):
                return None
        
        # Float columns
        if column in ['danceability', 'energy', 'loudness', 'acousticness', 
                      'instrumentalness', 'liveness', 'valence', 'tempo']:
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # String columns (id, title)
        return str(value)
    
    @staticmethod
    def load_data_to_db(normalized_data: List[Dict[str, Any]], batch_size: int = 100) -> int:
        """
        Load normalized data into the database.
        
        Args:
            normalized_data: List of normalized song records
            batch_size: Number of records to insert at once
            
        Returns:
            Number of records inserted
        """
        try:
            inserted_count = 0
            

            
            # Insert in batches
            for i in range(0, len(normalized_data), batch_size):
                batch = normalized_data[i:i + batch_size]
                
                for record in batch:
                    # Check if song already exists
                    existing_song = Song.query.filter_by(id=record.get('id')).first()
                    
                    if existing_song:
                        # Update existing song
                        for key, value in record.items():
                            if key == 'class':
                                setattr(existing_song, 'class_field', value)
                            elif hasattr(existing_song, key):
                                setattr(existing_song, key, value)
                    else:
                        # Create new song
                        song_data = record.copy()
                        if 'class' in song_data:
                            song_data['class_field'] = song_data.pop('class')
                        
                        song = Song(**song_data)
                        db.session.add(song)
                        inserted_count += 1
                
                # Commit batch
                db.session.commit()
                logger.info(f"Inserted batch {i // batch_size + 1}: {len(batch)} records")
            
            logger.info(f"Successfully loaded {inserted_count} new records to database")
            return inserted_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error loading data to database: {str(e)}")
            raise
    
    @staticmethod
    def process_json_file(file_path: str) -> int:
        """
        Process a JSON file and load it into the database.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Number of records inserted
        """
        try:
            # Read JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            logger.info(f"Loaded JSON file: {file_path}")
            
            # Normalize data
            normalized_data = DataProcessor.normalize_json(json_data)
            
            # Load to database
            inserted_count = DataProcessor.load_data_to_db(normalized_data)
            
            return inserted_count
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise

