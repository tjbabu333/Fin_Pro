"""
floating_admin_panel.py

Floating Admin Panel for Movie Review AI

Features
--------
✓ Floating Admin Button
✓ Collapsible Controls
✓ Backend Controls
✓ Frontend Controls
✓ Live Status
✓ Auto Refresh
✓ Notifications
✓ Modern Streamlit UI
"""

import streamlit as st

from api_client import APIClient
from state import AppState

api = APIClient()


class FloatingAdminPanel:

    @staticmethod
    def render():

        # Floating popover (works like your React floating panel)
        with st.popover("⚙️ Admin Controls", use_container_width=True):

            st.subheader("System Administration")

            ###########################################
            # Frontend Controls
            ###########################################

            st.markdown("### 🌐 Frontend")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Toggle Frontend Health",
                    use_container_width=True
                ):

                    AppState.toggle_frontend()

                    AppState.notify(
                        "Frontend health toggled",
                        "success"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Toggle Frontend Overload",
                    use_container_width=True
                ):

                    AppState.toggle_frontend_overload()

                    AppState.notify(
                        "Frontend overload toggled",
                        "warning"
                    )

                    st.rerun()

            st.divider()

            ###########################################
            # Backend Controls
            ###########################################

            st.markdown("### ⚙ Backend")

            if st.button(
                "Toggle Backend Health",
                use_container_width=True
            ):

                api.toggle_backend()

                AppState.notify(
                    "Backend toggled",
                    "success"
                )

                st.rerun()

            if st.button(
                "Toggle Backend Overload",
                use_container_width=True
            ):

                api.toggle_overload()

                AppState.notify(
                    "Backend overload toggled",
                    "warning"
                )

                st.rerun()

            if st.button(
                "Toggle Database",
                use_container_width=True
            ):

                api.toggle_database()

                AppState.notify(
                    "Database toggled",
                    "info"
                )

                st.rerun()

            if st.button(
                "Toggle Model Server",
                use_container_width=True
            ):

                api.toggle_model()

                AppState.notify(
                    "Model server toggled",
                    "info"
                )

                st.rerun()

            st.divider()

            ###########################################
            # System Status
            ###########################################

            st.markdown("### 📊 Live Status")

            try:

                status = api.backend_status()

                st.json(status)

            except Exception:

                st.error("Unable to connect to backend")

            st.divider()

            ###########################################
            # Refresh
            ###########################################

            if st.button(
                "🔄 Refresh Status",
                use_container_width=True
            ):

                st.rerun()

            ###########################################
            # Notifications
            ###########################################

            if st.session_state.notifications:

                st.markdown("### 🔔 Notifications")

                for notification in reversed(
                        st.session_state.notifications[-5:]
                ):

                    if notification.level == "success":
                        st.success(notification.message)

                    elif notification.level == "warning":
                        st.warning(notification.message)

                    elif notification.level == "error":
                        st.error(notification.message)

                    else:
                        st.info(notification.message)