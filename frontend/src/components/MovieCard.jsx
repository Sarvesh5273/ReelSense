import React from "react";
import { motion } from "framer-motion";

function MovieCard({ movie, isSkeleton = false }) {
  if (isSkeleton) {
    return (
      <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden animate-pulse">
        <div className="w-full h-64 bg-gray-700"></div>
        <div className="p-4 space-y-2">
          <div className="h-4 bg-gray-700 rounded"></div>
          <div className="h-3 bg-gray-700 rounded w-2/3"></div>
          <div className="h-2 bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }

  if (!movie) return null;

  const posterUrl =
    movie.poster ||
    "https://via.placeholder.com/300x450?text=No+Poster";

  const rating = Number(movie.predicted_rating || 0).toFixed(2);
  const match = Number(movie.match_percentage || 0).toFixed(1);

  return (
    <motion.div
      className="bg-gray-800 rounded-lg shadow-lg overflow-hidden relative group cursor-pointer"
      whileHover={{ scale: 1.05 }}
      transition={{ duration: 0.2 }}
    >
      {/* Poster */}
      <img
        src={posterUrl}
        alt={movie.title}
        className="w-full h-64 object-cover"
      />

      {/* Card Content */}
      <div className="p-4">
        <h3 className="text-lg font-semibold truncate">
          {movie.title}
        </h3>

        {/* Rating */}
        <div className="flex items-center mt-1 text-sm">
          <span className="text-yellow-400 mr-1">⭐</span>
          <span>{rating}</span>
        </div>

        {/* Match Score */}
        <div className="mt-2">
          <span className="text-sm text-red-500">
            🎯 {match}% Match
          </span>
          <div className="w-full bg-gray-700 rounded-full h-2 mt-1">
            <div
              className="bg-red-600 h-2 rounded-full"
              style={{ width: `${match}%` }}
            />
          </div>
        </div>

        {/* Genres */}
        {movie.genres && movie.genres.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {movie.genres.slice(0, 3).map((g) => (
              <span
                key={g}
                className="text-xs bg-gray-700 px-2 py-1 rounded"
              >
                {g}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Hover Explanation */}
      <div className="absolute inset-0 bg-black bg-opacity-80 flex items-center justify-center text-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 px-4">
        <p className="text-sm text-gray-200 leading-relaxed">
          {movie.explanation}
        </p>
      </div>
    </motion.div>
  );
}

export default MovieCard;
