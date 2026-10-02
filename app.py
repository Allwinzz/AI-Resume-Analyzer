import streamlit as st
from pypdf import PdfReader
from io import BytesIO

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #9ca3af;
    margin-bottom: 30px;
}

.score-box {
    padding: 25px;
    border-radius: 15px;
    background: #172033;
    text-align: center;
    border: 1px solid #29364f;
}

.score-number {
    font-size: 48px;
    font-weight: 700;
    color: #38bdf8;
}

.info-card {
    padding: 20px;
    border-radius: 12px;
    background: #172033;
    border: 1px solid #29364f;
    margin-bottom: 15px;
}

.skill-good {
    color: #4ade80;
    font-weight: 600;
}

.skill-missing {
    color: #fbbf24;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your resume and get skill analysis, ATS insights and job recommendations.'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "👤 Enter your name",
        placeholder="Example: Antony Jesu Allwin J"
    )

with col2:
    resume_file = st.file_uploader(
        "📄 Upload your Resume PDF",
        type=["pdf"]
    )

analyze = st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True
)

# =========================================================
# SKILLS DATABASE
# =========================================================

skills = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "sql",
    "machine learning",
    "data science",
    "react",
    "node.js",
    "git",
    "github",
    "c++",
    "php",
    "flask",
    "django"
]

# =========================================================
# CORE SKILLS FOR SCORE
# =========================================================

core_skills = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "sql",
    "machine learning",
    "git",
    "react",
    "node.js"
]

# =========================================================
# JOB ROLES
# =========================================================

job_roles = {

    "Web Developer": {
        "skills": [
            "html",
            "css",
            "javascript",
            "sql"
        ],
        "description":
            "Build and maintain websites and web applications."
    },

    "Machine Learning Engineer": {
        "skills": [
            "python",
            "machine learning",
            "sql"
        ],
        "description":
            "Build and work with machine learning models."
    },

    "Full Stack Developer": {
        "skills": [
            "html",
            "css",
            "javascript",
            "react",
            "node.js",
            "sql",
            "git"
        ],
        "description":
            "Develop both frontend and backend web applications."
    },

    "Python Developer": {
        "skills": [
            "python",
            "sql",
            "git",
            "flask",
            "django"
        ],
        "description":
            "Develop applications and backend systems using Python."
    },

    "Data Analyst": {
        "skills": [
            "python",
            "sql",
            "data science"
        ],
        "description":
            "Analyze data and generate useful business insights."
    }
}

# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if not name.strip():

        st.warning("⚠️ Please enter your name.")

    elif resume_file is None:

        st.warning("⚠️ Please upload your Resume PDF.")

    else:

        try:

            # =================================================
            # READ PDF
            # =================================================

            reader = PdfReader(resume_file)

            resume_text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    resume_text += page_text + "\n"

            text_lower = resume_text.lower()

            # =================================================
            # SUCCESS MESSAGE
            # =================================================

            st.success(
                f"Resume uploaded successfully, {name}! ✅"
            )

            # =================================================
            # RESUME ANALYSIS
            # =================================================

            st.header("📋 Resume Analysis")

            st.subheader("👤 Candidate")

            st.write(f"**{name}**")

            # =================================================
            # SKILL DETECTION
            # =================================================

            found_skills = []

            for skill in skills:

                if skill in text_lower:

                    found_skills.append(skill)

            st.subheader("🛠️ Skills Detected")

            if found_skills:

                skill_columns = st.columns(3)

                for index, skill in enumerate(found_skills):

                    with skill_columns[index % 3]:

                        st.success(
                            f"✅ {skill.title()}"
                        )

            else:

                st.info(
                    "No common technical skills detected."
                )

            # =================================================
            # RESUME SECTIONS
            # =================================================

            section_keywords = {

                "Career Objective": [
                    "career objective",
                    "objective"
                ],

                "Education": [
                    "education",
                    "academic"
                ],

                "Skills": [
                    "skills",
                    "technical skills"
                ],

                "Projects": [
                    "projects",
                    "project"
                ],

                "Certificates": [
                    "certificates",
                    "certifications",
                    "certificate"
                ],

                "Experience": [
                    "experience",
                    "work experience",
                    "internship"
                ]
            }

            detected_sections = []

            for section, keywords in section_keywords.items():

                for keyword in keywords:

                    if keyword in text_lower:

                        detected_sections.append(section)

                        break

            # =================================================
            # SCORE CALCULATION
            # =================================================

            core_found = 0

            for skill in core_skills:

                if skill in found_skills:

                    core_found += 1

            technical_score = int(
                (core_found / len(core_skills)) * 40
            )

            section_score = int(
                (len(detected_sections) / len(section_keywords)) * 60
            )

            total_score = technical_score + section_score

            # =================================================
            # SCORE
            # =================================================

            st.subheader("📊 Resume Score")

            score_col1, score_col2 = st.columns([1, 2])

            with score_col1:

                st.markdown(
                    f"""
                    <div class="score-box">
                        <div class="score-number">
                            {total_score}/100
                        </div>
                        <div>
                            Resume Score
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with score_col2:

                st.write("### Score Breakdown")

                st.write(
                    f"🛠️ **Technical Skills:** "
                    f"{technical_score}/40"
                )

                st.progress(
                    technical_score / 40
                )

                st.write(
                    f"📄 **Resume Sections:** "
                    f"{section_score}/60"
                )

                st.progress(
                    section_score / 60
                )

            # =================================================
            # DETECTED SECTIONS
            # =================================================

            if detected_sections:

                st.write(
                    "### ✅ Detected Resume Sections"
                )

                st.write(
                    ", ".join(detected_sections)
                )

            # =================================================
            # SKILLS TO ADD
            # =================================================

            missing_skills = []

            for skill in skills:

                if skill not in found_skills:

                    missing_skills.append(skill)

            st.subheader("⚠️ Skills You Can Add")

            if missing_skills:

                skill_columns = st.columns(4)

                for index, skill in enumerate(
                    missing_skills[:8]
                ):

                    with skill_columns[index % 4]:

                        st.write(
                            f"🔸 {skill.title()}"
                        )

            else:

                st.success(
                    "🎉 All listed skills were detected!"
                )

            # =================================================
            # JOB RECOMMENDATIONS
            # =================================================

            st.header("💼 Job Recommendations")

            recommendations = []

            for role, details in job_roles.items():

                required_skills = details["skills"]

                matched_skills = []

                missing_role_skills = []

                for skill in required_skills:

                    if skill in found_skills:

                        matched_skills.append(skill)

                    else:

                        missing_role_skills.append(skill)

                match_percentage = int(
                    (
                        len(matched_skills)
                        /
                        len(required_skills)
                    ) * 100
                )

                recommendations.append(
                    (
                        role,
                        match_percentage,
                        matched_skills,
                        missing_role_skills,
                        details["description"]
                    )
                )

            recommendations.sort(
                key=lambda x: x[1],
                reverse=True
            )

            # =================================================
            # DISPLAY JOBS
            # =================================================

            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                role = recommendation[0]

                match_percentage = recommendation[1]

                matched_skills = recommendation[2]

                missing_role_skills = recommendation[3]

                description = recommendation[4]

                with st.container(border=True):

                    st.markdown(
                        f"### {index}. 💼 {role}"
                    )

                    st.write(
                        f"**Skill Match: "
                        f"{match_percentage}%**"
                    )

                    st.progress(
                        match_percentage / 100
                    )

                    st.write(
                        f"📝 {description}"
                    )

                    if matched_skills:

                        st.write(
                            "✅ **Your Matching Skills:**"
                        )

                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in matched_skills
                            )
                        )

                    if missing_role_skills:

                        st.write(
                            "⚠️ **Skills You Need to Learn:**"
                        )

                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in missing_role_skills
                            )
                        )

            # =================================================
            # RESUME INFORMATION
            # =================================================

            st.header("📄 Resume Information")

            word_count = len(
                resume_text.split()
            )

            st.write(
                f"**Approximate Word Count:** "
                f"{word_count}"
            )

            # =================================================
            # EXTRACTED TEXT
            # =================================================

            st.subheader("📑 Extracted Resume Text")

            st.text_area(
                "Resume Content",
                resume_text,
                height=300
            )

            # =================================================
            # ATS ANALYSIS
            # =================================================

            st.header("🤖 ATS Analysis")

            ats_keywords = [
                "python",
                "java",
                "javascript",
                "html",
                "css",
                "sql",
                "git",
                "machine learning",
                "projects",
                "education",
                "skills",
                "certificates"
            ]

            ats_found = []

            for keyword in ats_keywords:

                if keyword in text_lower:

                    ats_found.append(keyword)

            ats_score = int(
                (
                    len(ats_found)
                    /
                    len(ats_keywords)
                ) * 100
            )

            st.write(
                f"**ATS Keyword Score: "
                f"{ats_score}/100**"
            )

            st.progress(
                ats_score / 100
            )

            if ats_score >= 70:

                st.success(
                    "✅ Good keyword coverage for ATS."
                )

            elif ats_score >= 40:

                st.warning(
                    "⚠️ Moderate ATS keyword coverage."
                )

            else:

                st.error(
                    "❌ Low ATS keyword coverage."
                )

            # =================================================
            # IMPROVEMENT SUGGESTIONS
            # =================================================

            st.header("💡 Resume Improvement Suggestions")

            suggestions = []

            if "projects" not in text_lower:

                suggestions.append(
                    "Add a Projects section with 2–3 practical projects."
                )

            if "experience" not in text_lower:

                suggestions.append(
                    "Add internship or practical experience if available."
                )

            if "sql" not in text_lower:

                suggestions.append(
                    "Consider adding SQL if you have database knowledge."
                )

            if "github" not in text_lower:

                suggestions.append(
                    "Add your GitHub profile to showcase projects."
                )

            if "linkedin" not in text_lower:

                suggestions.append(
                    "Add your LinkedIn profile to your resume."
                )

            if len(resume_text.split()) < 200:

                suggestions.append(
                    "Your resume is quite short. Add relevant projects, "
                    "certifications and technical details."
                )

            if suggestions:

                for suggestion in suggestions:

                    st.info(
                        f"💡 {suggestion}"
                    )

            else:

                st.success(
                    "🎉 Your resume contains the major recommended sections."
                )

            # =================================================
            # DOWNLOAD REPORT
            # =================================================

            st.header("📥 Download Report")

            report_text = f"""
AI RESUME ANALYZER REPORT
=========================

Candidate:
{name}

RESUME SCORE
------------
Overall Score: {total_score}/100
Technical Skills: {technical_score}/40
Resume Sections: {section_score}/60

DETECTED SKILLS
---------------
{", ".join(skill.title() for skill in found_skills)}

DETECTED RESUME SECTIONS
------------------------
{", ".join(detected_sections)}

SKILLS YOU CAN ADD
------------------
{", ".join(skill.title() for skill in missing_skills[:8])}

JOB RECOMMENDATIONS
-------------------

"""

            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                report_text += (
                    f"{index}. {recommendation[0]} - "
                    f"{recommendation[1]}%\n"
                )

            report_text += f"""

ATS ANALYSIS
------------
ATS Keyword Score: {ats_score}/100

APPROXIMATE WORD COUNT
----------------------
{word_count}

RESUME IMPROVEMENT SUGGESTIONS
------------------------------
"""

            for suggestion in suggestions:

                report_text += (
                    f"- {suggestion}\n"
                )

            report_bytes = BytesIO(
                report_text.encode("utf-8")
            )

            st.download_button(
                label="📥 Download Analysis Report",
                data=report_bytes,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )

            # =================================================
            # COMPLETION
            # =================================================

            st.success(
                "🎉 Resume analysis completed successfully!"
            )

        except Exception as e:

            st.error(
                f"❌ Error while reading the PDF: {e}"
            )