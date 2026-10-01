"""
Movie Database
--------------

Enhanced Python version of the React movie list.

Enhancements
------------
✓ Dataclass model
✓ Type hints
✓ Immutable movie objects
✓ Search utilities
✓ Lookup by ID
✓ Filter by genre
✓ Dictionary cache for O(1) lookup
✓ Easy to extend
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


# =====================================================
# Movie Model
# =====================================================

@dataclass(frozen=True)
class Movie:
    id: str
    title: str
    thumbnail: str
    year: int
    genre: str

    @property
    def image_exists(self) -> bool:
        """Check whether thumbnail exists locally."""
        return Path(self.thumbnail).exists()

    @property
    def display_name(self) -> str:
        return f"{self.title} ({self.year})"

    @property
    def short_info(self) -> str:
        return f"{self.genre} • {self.year}"


# =====================================================
# Movie Database
# =====================================================

MOVIES: List[Movie] = [

    Movie(
        id="shawshank",
        title="The Shawshank Redemption",
        thumbnail="images/movies/shawshank-redemption.jpg",
        year=1994,
        genre="Drama",
    ),

    Movie(
        id="inception",
        title="Inception",
        thumbnail="images/movies/inception.jpg",
        year=2010,
        genre="Sci-Fi",
    ),

    Movie(
        id="interstellar",
        title="Interstellar",
        thumbnail="images/movies/interstellar.jpg",
        year=2014,
        genre="Sci-Fi",
    ),

    Movie(
        id="fight-club",
        title="Fight Club",
        thumbnail="images/movies/fight-club.jpg",
        year=1999,
        genre="Drama",
    ),

    Movie(
        id="gladiator",
        title="Gladiator",
        thumbnail="images/movies/gladiator.jpg",
        year=2000,
        genre="Action",
    ),

    Movie(
        id="dark-knight",
        title="The Dark Knight",
        thumbnail="images/movies/dark-knight.jpg",
        year=2008,
        genre="Action",
    ),
]

# =====================================================
# Fast Lookup Cache
# =====================================================

_MOVIE_MAP = {movie.id: movie for movie in MOVIES}


# =====================================================
# Helper Functions
# =====================================================

def get_movie(movie_id: str) -> Optional[Movie]:
    """Return movie by ID."""
    return _MOVIE_MAP.get(movie_id)


def get_movie_title(movie_id: str) -> str:
    """Return title from movie ID."""
    movie = get_movie(movie_id)
    return movie.title if movie else movie_id


def all_movies() -> List[Movie]:
    """Return all movies."""
    return MOVIES.copy()


def movies_by_genre(genre: str) -> List[Movie]:
    """Filter movies by genre."""
    genre = genre.lower()

    return [
        movie
        for movie in MOVIES
        if movie.genre.lower() == genre
    ]


def search_movies(keyword: str) -> List[Movie]:
    """Search movies by title."""

    keyword = keyword.lower()

    return [
        movie
        for movie in MOVIES
        if keyword in movie.title.lower()
    ]


def latest_movie() -> Movie:
    """Newest movie."""
    return max(MOVIES, key=lambda m: m.year)


def oldest_movie() -> Movie:
    """Oldest movie."""
    return min(MOVIES, key=lambda m: m.year)


def movie_statistics():
    """Return movie collection statistics."""

    genres = {}

    for movie in MOVIES:
        genres[movie.genre] = genres.get(movie.genre, 0) + 1

    return {
        "total_movies": len(MOVIES),
        "genres": genres,
        "oldest": oldest_movie().display_name,
        "newest": latest_movie().display_name,
    }


# =====================================================
# Demo
# =====================================================

if __name__ == "__main__":

    print("Movie Collection\n")

    for movie in MOVIES:
        print(movie.display_name)

    print("\nStatistics")
    print(movie_statistics())