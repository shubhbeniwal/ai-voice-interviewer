import streamlit as st
import html


def speak(text: str):
    safe_text = html.escape(text)

    st.components.v1.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{safe_text}");
            msg.rate = 1;
            msg.pitch = 1;
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)