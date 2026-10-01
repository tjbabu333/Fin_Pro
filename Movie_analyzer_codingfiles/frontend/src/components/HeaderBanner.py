"""
Header Banner Component
Enhanced Streamlit Version
Author: AI Conversion

Features
--------
✔ Modern gradient banner
✔ Animated title
✔ Technology badges
✔ Responsive layout
✔ Better typography
✔ Easy customization
"""

import streamlit as st


class HeaderBanner:
    """Beautiful application header"""

    @staticmethod
    def render():
        st.markdown(
            """
<style>

.banner{
    background:linear-gradient(135deg,#0f172a,#1d4ed8,#7c3aed);
    border-radius:20px;
    padding:35px;
    margin-bottom:25px;
    color:white;
    box-shadow:0 10px 35px rgba(0,0,0,.25);
    text-align:center;
    animation:fadeIn 0.8s ease;
}

.banner h1{
    font-size:48px;
    margin-bottom:5px;
}

.banner h2{
    font-size:22px;
    color:#dbeafe;
    margin-top:0;
}

.banner p{
    font-size:18px;
    color:#f8fafc;
}

.badges{
    margin-top:18px;
}

.badge{
    display:inline-block;
    margin:5px;
    padding:8px 16px;
    border-radius:25px;
    background:rgba(255,255,255,.15);
    border:1px solid rgba(255,255,255,.25);
    font-weight:bold;
    backdrop-filter: blur(10px);
}

@keyframes fadeIn{
from{
opacity:0;
transform:translateY(-20px);
}
to{
opacity:1;
transform:translateY(0);
}
}

</style>

<div class="banner">

<h1>🎬 Movie Review Platform</h1>

<h2>AI Powered Movie Sentiment Analysis</h2>

<p>
DevOps • Kubernetes • Docker • FastAPI • PostgreSQL • Machine Learning
</p>

<div class="badges">

<span class="badge">🚀 FastAPI</span>

<span class="badge">🤖 AI Analysis</span>

<span class="badge">🐳 Docker</span>

<span class="badge">☸ Kubernetes</span>

<span class="badge">🗄 PostgreSQL</span>

<span class="badge">📊 Streamlit</span>

</div>

</div>
""",
            unsafe_allow_html=True,
        )