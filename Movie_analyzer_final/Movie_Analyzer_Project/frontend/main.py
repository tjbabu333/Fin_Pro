from __future__ import annotations

import os
from pathlib import Path

import httpx
from nicegui import app, ui

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

MOVIES = [
    {"id": "Peddi", "title": "Peddi", "year": 2026, "genre": "Sports Drama", "image": "Peddi.jpg"},
    {"id": "shawshank", "title": "The Shawshank Redemption", "year": 1994, "genre": "Drama", "image": "shawshank-redemption.jpg"},
    {"id": "inception", "title": "Inception", "year": 2010, "genre": "Sci-Fi", "image": "inception.jpg"},
    {"id": "interstellar", "title": "Interstellar", "year": 2014, "genre": "Sci-Fi", "image": "interstellar.jpg"},
    {"id": "fight-club", "title": "Fight Club", "year": 1999, "genre": "Drama", "image": "fight-club.jpg"},
    {"id": "gladiator", "title": "Gladiator", "year": 2000, "genre": "Action", "image": "gladiator.jpg"},
    {"id": "dark-knight", "title": "The Dark Knight", "year": 2008, "genre": "Action", "image": "dark-knight.jpg"},
]
MOVIE_BY_ID = {m["id"]: m for m in MOVIES}

images_dir = Path(__file__).parent / "images"
app.add_static_files("/images", images_dir)


async def api_get(path: str):
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(f"{BACKEND_URL}{path}")
        response.raise_for_status()
        return response.json()


async def api_post(path: str, payload: dict):
    async with httpx.AsyncClient(timeout=8.0) as client:
        response = await client.post(f"{BACKEND_URL}{path}", json=payload)
        response.raise_for_status()
        return response.json()


@ui.page("/")
def home_page():
    selected = {"movie_id": "shawshank"}

    with ui.column().classes("w-full items-center gap-4 p-4"):
        ui.label("🎬 Movie Analyzer").classes("text-4xl font-bold")
        ui.label("Submit a review and get sentiment + an AI-style star rating.").classes("text-lg text-gray-600")

        health_label = ui.label("Checking services...").classes("text-sm")

        async def refresh_health():
            try:
                data = await api_get("/health")
                health_label.set_text(
                    f"Backend: {'UP' if data['backend'] else 'DOWN'} | "
                    f"Database: {'UP' if data['database'] else 'DOWN'} | "
                    f"Model: {'UP' if data['model'] else 'DOWN'}"
                )
            except Exception:
                health_label.set_text("Backend is unavailable")

        ui.timer(0.2, refresh_health, once=True)
        ui.timer(10, refresh_health)

        detail = ui.column().classes("w-full max-w-4xl")
        latest = ui.column().classes("w-full max-w-4xl")

        async def render_latest():
            latest.clear()
            with latest:
                ui.label("Latest Reviews").classes("text-2xl font-semibold")
                try:
                    rows = await api_get("/api/reviews/latest?limit=5")
                except Exception:
                    ui.label("Could not load latest reviews.")
                    return
                for row in rows:
                    movie = MOVIE_BY_ID.get(row["movieId"], {"title": row["movieId"]})
                    with ui.card().classes("w-full"):
                        ui.label(movie["title"]).classes("font-semibold")
                        ui.label(row["reviewText"])
                        ui.label(f"{row['sentiment']} • {row['rating']} ⭐").classes("text-sm")

        async def open_movie(movie_id: str):
            selected["movie_id"] = movie_id
            movie = MOVIE_BY_ID[movie_id]
            detail.clear()
            try:
                reviews = await api_get(f"/api/reviews/{movie_id}")
            except Exception:
                reviews = []

            with detail:
                with ui.row().classes("w-full items-start gap-6"):
                    ui.image(f"/images/movies/{movie['image']}").classes("w-48 rounded-lg")
                    with ui.column().classes("flex-1"):
                        ui.label(movie["title"]).classes("text-3xl font-bold")
                        ui.label(f"{movie['genre']} • {movie['year']}")
                        review_input = ui.textarea(
                            label="Your review",
                            placeholder="Example: The acting was amazing and the story kept me engaged...",
                        ).classes("w-full")

                        async def submit():
                            review_text = (review_input.value or "").strip()
                            if len(review_text) < 3:
                                ui.notify("Please enter a review.", type="warning")
                                return
                            try:
                                result = await api_post(
                                    "/api/reviews",
                                    {"movieId": movie_id, "reviewText": review_text},
                                )
                                ui.notify(
                                    f"{result['sentiment'].title()} • {result['rating']} stars",
                                    type="positive",
                                )
                                review_input.value = ""
                                await open_movie(movie_id)
                                await render_latest()
                            except Exception as exc:
                                ui.notify(f"Submission failed: {exc}", type="negative")

                        ui.button("Analyze & Save Review", on_click=submit)

                ui.separator()
                ui.label("Review History").classes("text-2xl font-semibold")
                if not reviews:
                    ui.label("No reviews yet.")
                for row in reviews:
                    with ui.card().classes("w-full"):
                        ui.label(row["reviewText"])
                        ui.label(
                            f"Sentiment: {row['sentiment']} | Score: {row['sentimentScore']} | Rating: {row['rating']} ⭐"
                        ).classes("text-sm")

        ui.label("Movies").classes("text-2xl font-semibold")
        with ui.row().classes("w-full max-w-6xl justify-center gap-4"):
            for movie in MOVIES:
                with ui.card().classes("w-48 cursor-pointer") as card:
                    ui.image(f"/images/movies/{movie['image']}").classes("w-full h-64 object-cover")
                    ui.label(movie["title"]).classes("font-semibold")
                    ui.label(f"{movie['genre']} • {movie['year']}").classes("text-sm")
                    card.on("click", lambda _, movie_id=movie["id"]: open_movie(movie_id))

        ui.timer(0.1, lambda: open_movie(selected["movie_id"]), once=True)
        ui.timer(0.1, render_latest, once=True)


ui.run(host="0.0.0.0", port=3000, title="Movie Analyzer", reload=False)
