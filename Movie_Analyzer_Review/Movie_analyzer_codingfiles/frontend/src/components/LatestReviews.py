"""
Latest Reviews Component
------------------------
Displays the latest community reviews.

Enhanced Features
-----------------
✓ Beautiful cards
✓ Sentiment colors
✓ Star rating
✓ Expandable reviews
✓ Relative dates
✓ Statistics
✓ Empty state
"""

from datetime import datetime
import streamlit as st

from data.movies import MOVIES


class LatestReviews:

    @staticmethod
    def movie_title(movie_id: str) -> str:
        for movie in MOVIES:
            if movie["id"] == movie_id:
                return movie["title"]
        return movie_id

    @staticmethod
    def sentiment_color(sentiment):

        sentiment = (sentiment or "").lower()

        if sentiment == "positive":
            return "🟢", "#16a34a"

        if sentiment == "negative":
            return "🔴", "#dc2626"

        return "🟡", "#d97706"

    @staticmethod
    def format_date(date_string):

        try:
            dt = datetime.fromisoformat(date_string.replace("Z", ""))

            return dt.strftime("%b %d, %Y")

        except Exception:
            return "Recent"

    @staticmethod
    def render(latest_reviews):

        st.markdown("## 📝 Latest Community Reviews")

        if not latest_reviews:

            st.info("No reviews available yet.\n\nBe the first to review a movie!")

            return

        # ---------- Statistics ----------

        total = len(latest_reviews)

        positives = len(
            [r for r in latest_reviews
             if r.get("sentiment") == "positive"]
        )

        negatives = len(
            [r for r in latest_reviews
             if r.get("sentiment") == "negative"]
        )

        avg_rating = (
            sum(r.get("rating", 0) for r in latest_reviews)
            / total
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Reviews", total)
        c2.metric("Positive", positives)
        c3.metric("Negative", negatives)
        c4.metric("Average Rating", f"{avg_rating:.1f} ⭐")

        st.divider()

        # ---------- Review Cards ----------

        for review in latest_reviews:

            icon, color = LatestReviews.sentiment_color(
                review.get("sentiment")
            )

            movie = LatestReviews.movie_title(
                review.get("movieId")
            )

            with st.container(border=True):

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.markdown(
                        f"### 🎬 {movie}"
                    )

                with col2:

                    st.metric(
                        "⭐",
                        f"{review.get('rating',0):.1f}"
                    )

                st.markdown(
                    f"""
<span style='color:{color};
font-weight:bold;
font-size:16px'>
{icon} {review.get("sentiment","Neutral").title()}
</span>

&nbsp;&nbsp;&nbsp;

🗓️ {LatestReviews.format_date(review.get("createdAt",""))}
""",
                    unsafe_allow_html=True,
                )

                text = review.get("reviewText", "")

                if len(text) > 250:

                    with st.expander("Read Review"):

                        st.write(text)

                else:

                    st.write(f"💬 *{text}*")

        st.success(
            "💡 Select a movie to add your own review with AI sentiment analysis."
        )