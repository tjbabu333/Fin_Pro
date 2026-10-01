"""
Movie Detail Page
-----------------
Shows

✓ Movie information
✓ Review submission
✓ Latest AI analysis
✓ Review history
✓ Service status

Enhanced Streamlit version
"""

import streamlit as st

from components.review_form import ReviewForm
from components.review_history import ReviewHistory
from components.latest_analysis import LatestAnalysis


class MovieDetail:

    @staticmethod
    def render(
        movie,
        reviews,
        service_status,
        latest_analysis,
        submit_callback
    ):

        if st.button("⬅ Back to Movies"):
            st.session_state.selected_movie = None
            st.rerun()

        st.divider()

        MovieDetail.show_movie(movie)

        MovieDetail.show_service_status(service_status)

        ReviewForm.render(
            movie,
            service_status,
            submit_callback
        )

        if (
            latest_analysis
            and latest_analysis.get("movieId") == movie["id"]
        ):
            LatestAnalysis.render(latest_analysis)

        ReviewHistory.render(
            movie,
            reviews,
            service_status
        )

    @staticmethod
    def show_movie(movie):

        c1, c2 = st.columns([1,3])

        with c1:

            if movie.get("thumbnail"):

                st.image(
                    movie["thumbnail"],
                    use_container_width=True
                )

            else:

                st.image(
                    "https://placehold.co/300x450?text=Movie"
                )

        with c2:

            st.title(movie["title"])

            st.write(f"**Year:** {movie['year']}")

            st.write(f"**Genre:** {movie['genre']}")

            st.caption(movie["id"])

    @staticmethod
    def show_service_status(status):

        backend = status["backend"]
        db = status["database"]
        model = status["model"]

        if not backend:

            st.error(
                "Backend unavailable. Review submission disabled."
            )

        elif not db and not model:

            st.warning(
                "Database and AI model unavailable."
            )

        elif not db:

            st.warning(
                "Database unavailable.\n\nReviews will be analyzed but not saved."
            )

        elif not model:

            st.warning(
                "AI Model unavailable.\n\nSentiment analysis disabled."
            )

        else:

            st.success("All services operational.")

import streamlit as st


class ReviewForm:

    @staticmethod
    def render(movie, status, callback):

        st.subheader(
            f"✍ Review {movie['title']}"
        )

        disabled = not status["backend"]

        review = st.text_area(
            "Your Review",
            key=f"review_{movie['id']}",
            height=150,
            disabled=disabled
        )

        if st.button(
            "Submit Review",
            disabled=disabled or review == ""
        ):

            callback(movie["id"], review)

import streamlit as st


class LatestAnalysis:

    @staticmethod
    def render(result):

        st.subheader("🎯 AI Analysis")

        c1,c2,c3=st.columns(3)

        with c1:

            emoji={
                "positive":"😊",
                "neutral":"😐",
                "negative":"😞"
            }

            st.metric(
                "Sentiment",
                emoji.get(
                    result["sentiment"],
                    "😐"
                )
            )

        with c2:

            st.metric(
                "Rating",
                f'{result["rating"]:.1f}/5'
            )

        with c3:

            st.metric(
                "Confidence",
                f'{result["sentimentScore"]*100:.0f}%'
            )

        st.info(result["reviewText"])

import streamlit as st


class ReviewHistory:

    @staticmethod
    def render(movie,reviews,status):

        st.subheader(
            f"📖 Reviews ({len(reviews)})"
        )

        if not status["backend"]:

            st.error(
                "Backend unavailable."
            )
            return

        if not status["database"]:

            st.error(
                "Database unavailable."
            )
            return

        if not reviews:

            st.info(
                "No reviews yet."
            )
            return

        for review in reviews:

            with st.container(border=True):

                st.write(
                    f'**"{review["reviewText"]}"**'
                )

                col1,col2,col3=st.columns(3)

                col1.write(
                    review["sentiment"].title()
                )

                col2.write(
                    f'⭐ {review["rating"]:.1f}'
                )

                col3.write(
                    f'Score {review["sentimentScore"]:.2f}'
                )
