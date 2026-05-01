# In app.py

st.subheader("📄 Your Resume")

tab_pdf, tab_paste = st.tabs(["Upload PDF", "Paste Text"])

with tab_pdf:
    resume_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="PDF files only. Multi-page resumes supported.",
        label_visibility="collapsed"
    )
    if resume_file:
        st.success(f"✅ {resume_file.name} uploaded")

with tab_paste:
    resume_pasted = st.text_area(
        "Paste resume content here",
        height=280,
        placeholder="Copy and paste your full resume text...",
        label_visibility="collapsed"
    )

# Resolve to a single clean string
resume_text, resume_source = get_resume_text(resume_file, resume_pasted)
