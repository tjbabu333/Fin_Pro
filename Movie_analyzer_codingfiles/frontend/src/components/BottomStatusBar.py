"""
bottom_status_bar.py

Reusable Bottom Status Bar for Movie Review AI

Features
--------
✓ Real-time health monitoring
✓ Service status cards
✓ Overall health summary
✓ Overload detection
✓ Last updated timestamp
✓ Streamlit compatible
"""

import streamlit as st
from datetime import datetime


class BottomStatusBar:

    @staticmethod
    def render(
        frontend_healthy=True,
        frontend_overloaded=False,
        backend_healthy=True,
        backend_overloaded=False,
        database_connected=True,
        model_connected=True
    ):

        services = [
            frontend_healthy,
            backend_healthy,
            database_connected,
            model_connected
        ]

        online = sum(services)

        overloaded = (
            frontend_overloaded or
            backend_overloaded
        )

        ###################################################
        # Overall Status
        ###################################################

        if online == 4 and not overloaded:
            status = "Healthy"
            color = "green"
            icon = "✅"

        elif online == 4 and overloaded:
            status = "Overloaded"
            color = "orange"
            icon = "⚡"

        elif online >= 2:
            status = "Partial Failure"
            color = "orange"
            icon = "⚠️"

        elif online == 1:
            status = "Major Outage"
            color = "red"
            icon = "🔴"

        else:
            status = "Critical Failure"
            color = "red"
            icon = "💥"

        ###################################################
        # Separator
        ###################################################

        st.divider()

        ###################################################
        # Status Cards
        ###################################################

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "🌐 Frontend",
                "Healthy" if frontend_healthy else "Offline",
                delta="Overloaded" if frontend_overloaded else "Normal"
            )

        with c2:

            st.metric(
                "⚙ Backend",
                "Healthy" if backend_healthy else "Offline",
                delta="Overloaded" if backend_overloaded else "Normal"
            )

        with c3:

            st.metric(
                "🗄 Database",
                "Connected" if database_connected else "Disconnected"
            )

        with c4:

            st.metric(
                "🤖 AI Model",
                "Online" if model_connected else "Offline"
            )

        ###################################################
        # Overall Health Banner
        ###################################################

        if color == "green":

            st.success(
                f"{icon} All Systems Operational"
            )

        elif color == "orange":

            st.warning(
                f"{icon} {status}"
            )

        else:

            st.error(
                f"{icon} {status}"
            )

        ###################################################
        # Health Percentage
        ###################################################

        percentage = (online / 4) * 100

        st.progress(percentage / 100)

        st.caption(
            f"System Health: {percentage:.0f}%"
        )

        ###################################################
        # Timestamp
        ###################################################

        st.caption(
            f"Last Updated : {datetime.now().strftime('%H:%M:%S')}"
        )