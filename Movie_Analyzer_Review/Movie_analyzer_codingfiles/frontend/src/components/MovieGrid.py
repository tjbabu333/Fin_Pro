"""
Movie Grid Component
--------------------

Enhanced Streamlit Version

Features
--------
✓ Responsive movie grid
✓ Movie posters
✓ Search support
✓ Genre filtering
✓ Click to open details
✓ Placeholder image fallback
✓ Better UI than React version
"""

import streamlit as st


class MovieGrid:

    @staticmethod
    def render(movies):

        st.markdown("## 🎬 Browse Movies")

        if not movies:
            st.warning("No movies available.")
            return

        # -----------------------------
        # Search Box
        # -----------------------------

        search = st.text_input(
            "🔍 Search Movies",
            placeholder="Search by title..."
        )

        # -----------------------------
        # Genre Filter
        # -----------------------------

        genres = sorted(
            list(
                set(movie["genre"] for movie in movies)
            )
        )

        genre = st.selectbox(
            "Genre",
            ["All"] + genres
        )

        filtered = []

        for movie in movies:

            if (
                search.lower() not in movie["title"].lower()
            ):
                continue

            if (
                genre != "All"
                and movie["genre"] != genre
            ):
                continue

            filtered.append(movie)

        # -----------------------------
        # Grid Layout
        # -----------------------------

        cols = st.columns(4)

        for index, movie in enumerate(filtered):

            with cols[index % 4]:

                MovieGrid.movie_card(movie)

    @staticmethod
    def movie_card(movie):

        poster = movie.get("thumbnail")

        if poster:

            st.image(
                poster,
                use_container_width=True
            )

        else:

            st.image(
                "https://placehold.co/300x450?text=🎬",
                use_container_width=True
            )

        st.markdown(
            f"### {movie['title']}"
        )

        st.caption(
            f"{movie['year']} • {movie['genre']}"
        )

        if st.button(
            "View Details",
            key=f"movie_{movie['id']}"
        ):

            st.session_state.selected_movie = movie
            st.rerun()