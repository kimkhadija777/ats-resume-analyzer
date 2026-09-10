import streamlit as st

from analyzer import analyze_resume
from resume_parser import extract_resume_text


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)


st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume and paste a job description to analyze "
    "how well your resume matches the job."
)

st.info(
    "This tool provides an AI-based estimate. "
    "It does not guarantee an interview or job offer."
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.header("⚙️ Settings")

    model = st.selectbox(
        "Choose Groq Model",
        [
            "openai/gpt-oss-120b",
            "qwen/qwen3.6-27b",
        ],
        index=0,
    )

    st.markdown("---")

    st.write("### Supported Resume Files")
    st.write("📄 PDF")
    st.write("📝 DOCX")


# -----------------------------
# Inputs
# -----------------------------

st.subheader("1️⃣ Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"],
)


st.subheader("2️⃣ Paste Job Description")

job_description = st.text_area(
    "Job Description",
    height=300,
    placeholder=(
        "Paste the complete job description here..."
    ),
)


# -----------------------------
# Analyze
# -----------------------------

analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True,
)


if analyze_button:

    if uploaded_file is None:
        st.error("Please upload a PDF or DOCX resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    try:
        with st.spinner("Reading your resume..."):

            resume_text = extract_resume_text(
                uploaded_file
            )

        if not resume_text.strip():
            st.error(
                "Could not extract readable text from the resume."
            )
            st.stop()

        with st.spinner(
            "AI is analyzing your resume against the job description..."
        ):

            result = analyze_resume(
                resume_text=resume_text,
                job_description=job_description,
                model=model,
            )

        st.success("Analysis completed successfully! 🎉")

        # -----------------------------
        # Match Score
        # -----------------------------

        st.subheader("🎯 Overall Match")

        score = result["match_score"]

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric(
                "Match Score",
                f"{score}%",
            )

        with col2:
            st.progress(score / 100)

        # -----------------------------
        # Final Result
        # -----------------------------

        st.subheader("📝 Final Result")

        st.write(
            f"**{result['final_result']['label']}**"
        )

        st.write(
            result["final_result"]["summary"]
        )

        # -----------------------------
        # Skills
        # -----------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matching Skills")

            matching_skills = result["matching_skills"]

            if matching_skills:
                for skill in matching_skills:
                    st.success(skill)
            else:
                st.write("No strong matching skills identified.")

        with col2:

            st.subheader("❌ Missing Skills")

            missing_skills = result["missing_skills"]

            if missing_skills:
                for skill in missing_skills:
                    st.warning(skill)
            else:
                st.success("No major missing skills identified.")

        # -----------------------------
        # ATS Keywords
        # -----------------------------

        st.subheader("🔑 ATS Keywords")

        keywords = result["ats_keywords"]

        for keyword in keywords:

            status = keyword["status"]

            if status == "found":
                st.success(
                    f"**{keyword['keyword']}** — Found"
                )

            elif status == "partial":
                st.warning(
                    f"**{keyword['keyword']}** — Partial"
                )

            else:
                st.error(
                    f"**{keyword['keyword']}** — Missing"
                )

        # -----------------------------
        # Problems
        # -----------------------------

        st.subheader("⚠️ Resume Problems")

        problems = result["problems"]

        if problems:

            for problem in problems:
                st.warning(
                    f"**{problem['problem']}**\n\n"
                    f"{problem['explanation']}"
                )

        else:
            st.success(
                "No major problems were identified."
            )

        # -----------------------------
        # Recommendations
        # -----------------------------

        st.subheader("💡 Recommendations")

        recommendations = result["recommendations"]

        for recommendation in recommendations:

            st.info(
                f"**{recommendation['recommendation']}**\n\n"
                f"{recommendation['reason']}"
            )

        # -----------------------------
        # Experience / Education
        # -----------------------------

        st.subheader("💼 Experience & Education")

        experience = result["experience_match"]

        st.write(
            f"**Experience:** {experience['status']}"
        )

        st.write(
            experience["explanation"]
        )

        education = result["education_match"]

        st.write(
            f"**Education:** {education['status']}"
        )

        st.write(
            education["explanation"]
        )

        # -----------------------------
        # Raw JSON
        # -----------------------------

        with st.expander("🔎 View Structured JSON"):

            st.json(result)

    except Exception as error:

        st.error(
            "Something went wrong while analyzing the resume."
        )

        st.exception(error)
