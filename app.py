import streamlit as st

st.set_page_config(page_title="MovieVerse UI", page_icon="🎬", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top, #1f1147 0%, #090013 55%, #040008 100%);
            color: white;
            overflow-x: hidden;
        }
        .hero {
            text-align: center;
            padding: 2rem 0 1rem 0;
        }
        .title {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: 1.4px;
            background: linear-gradient(90deg, #ff80bf, #84d7ff, #a0ffcb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2.4s ease-in-out infinite alternate;
        }
        .subtitle {
            font-size: 1rem;
            opacity: 0.9;
            margin-top: 0.5rem;
        }
        .glass {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 18px;
            padding: 1rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35);
        }
        .bubble {
            position: fixed;
            border-radius: 50%;
            pointer-events: none;
            opacity: 0.3;
            z-index: 0;
            animation: floatUp linear infinite;
            filter: blur(1px);
        }
        .bubble.one { width: 120px; height: 120px; left: 6%; background: #8a5bff; animation-duration: 12s; }
        .bubble.two { width: 150px; height: 150px; left: 28%; background: #00ffc8; animation-duration: 15s; animation-delay: 1.5s; }
        .bubble.three { width: 90px; height: 90px; left: 52%; background: #ff66c4; animation-duration: 10s; animation-delay: 3s; }
        .bubble.four { width: 180px; height: 180px; left: 75%; background: #4cb8ff; animation-duration: 18s; animation-delay: 2s; }
        .bubble.five { width: 70px; height: 70px; left: 88%; background: #ffd166; animation-duration: 8s; animation-delay: 4s; }
        @keyframes floatUp {
            from { transform: translateY(110vh) scale(0.8); }
            to { transform: translateY(-25vh) scale(1.2); }
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px rgba(255, 128, 191, 0.2), 0 0 18px rgba(132, 215, 255, 0.2); }
            to { text-shadow: 0 0 18px rgba(255, 128, 191, 0.7), 0 0 26px rgba(132, 215, 255, 0.65); }
        }
    </style>
    <div class="bubble one"></div>
    <div class="bubble two"></div>
    <div class="bubble three"></div>
    <div class="bubble four"></div>
    <div class="bubble five"></div>
    <div class="hero">
        <div class="title">MovieVerse Recommender</div>
        <div class="subtitle">Upload your model script + datasets and light up recommendations in style.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("🚀 Build Panel")
    uploaded_script = st.file_uploader(
        "Upload Python recommendation script",
        type=["py"],
        accept_multiple_files=False,
    )
    uploaded_data = st.file_uploader(
        "Upload dataset files",
        type=["csv", "xlsx", "json", "parquet"],
        accept_multiple_files=True,
    )
    favorite_genre = st.selectbox(
        "Pick your mood genre",
        ["Action", "Drama", "Sci-Fi", "Romance", "Thriller", "Comedy", "Mystery"],
    )
    energy = st.slider("Recommendation energy level", 1, 10, 7)
    recommend = st.button("✨ Launch Recommendations")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("🎥 Result Stage")
    if recommend:
        st.success("Frontend ready! Connect your backend logic to process uploaded files.")
        st.markdown(
            f"""
            **Current setup**
            - Genre focus: `{favorite_genre}`
            - Energy level: `{energy}`
            - Script uploaded: `{"Yes" if uploaded_script else "No"}`
            - Dataset count: `{len(uploaded_data) if uploaded_data else 0}`
            """
        )
        st.balloons()
    else:
        st.info("Upload files and click **Launch Recommendations** to preview the flow.")
    st.markdown("</div>", unsafe_allow_html=True)
