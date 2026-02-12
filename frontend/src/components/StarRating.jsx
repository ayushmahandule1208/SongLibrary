import React, { useState } from 'react';
import { Star } from 'lucide-react';
import './StarRating.css';

const StarRating = ({ rating = 0, songId, onRate }) => {
  const [hoveredRating, setHoveredRating] = useState(0);

  const handleClick = (newRating) => {
    if (onRate && songId) {
      onRate(songId, newRating);
    }
  };

  const handleMouseEnter = (starValue) => {
    setHoveredRating(starValue);
  };

  const handleMouseLeave = () => {
    setHoveredRating(0);
  };

  const displayRating = hoveredRating || rating;

  return (
    <div className="star-rating-container">
      {[1, 2, 3, 4, 5].map((starValue) => {
        const isFilled = starValue <= displayRating;
        return (
          <button
            key={starValue}
            type="button"
            className={`star-button ${isFilled ? 'filled' : ''}`}
            onClick={(e) => {
              e.stopPropagation();
              handleClick(starValue);
            }}
            onMouseEnter={() => handleMouseEnter(starValue)}
            onMouseLeave={handleMouseLeave}
            aria-label={`Rate ${starValue} out of 5 stars`}
          >
            <Star
              size={16}
              fill={isFilled ? 'currentColor' : 'none'}
              strokeWidth={isFilled ? 0 : 1.5}
            />
          </button>
        );
      })}
    </div>
  );
};

export default StarRating;

