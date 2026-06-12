import streamlit as st
from datetime import datetime, timedelta
import uuid
import json
from io import BytesIO

# ═══════════════════════════════════════════════════════════
# IMPORT CUSTOM MODULES
# ═══════════════════════════════════════════════════════════

try:
    from ai_assistant import AIAssistant
    from pdf_extractor import DocumentExtractor
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False
    st.warning("⚠️ Some AI features require configuration")

# ═══════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="OCSS - AI Student Organizer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════
# CUSTOM CSS (Professional Styling)
# ═══════════════════════════════════════════════════════════

st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    
    h1 {
        color: #2c3e50;
        border-bottom: 4px solid #3498db;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #34495e;
        margin-top: 2rem;
        border-left: 4px solid #3498db;
        padding-left: 1rem;
    }
    
    h3 {
        color: #7f8c8d;
        margin-top: 1.5rem;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background-color: #3498db !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.75rem 2rem !important;
        font-weight: bold !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background-color: #2980b9 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    .flashcard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        min-height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 1.1rem;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = ""

if 'semesters' not in st.session_state:
    st.session_state.semesters = {}

if 'current_semester' not in st.session_state:
    st.session_state.current_semester = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'mock_tests' not in st.session_state:
    st.session_state.mock_tests = {}

if 'study_logs' not in st.session_state:
    st.session_state.study_logs = []

# ═══════════════════════════════════════════════════════════
# 1. LOGIN PAGE
# ═══════════════════════════════════════════════════════════

def show_login_page():
    """User login and registration"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🎓 OCSS")
        st.markdown("## One Click Semester Setup")
        st.markdown("*AI-Powered Academic Organizer for Smart Students*")
        st.markdown("---")
        
        # Login tab
        tab1, tab2 = st.tabs(["📝 Login", "✍️ Register"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            login_username = st.text_input("Username", key="login_user", placeholder="Enter username")
            login_password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                if st.button("🔓 Login", use_container_width=True, key="login_btn"):
                    if login_username and login_password:
                        st.session_state.user_logged_in = True
                        st.session_state.username = login_username
                        st.success(f"✅ Welcome back, {login_username}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Please enter both username and password!")
            
            with col_login2:
                st.write("")
                st.write("")
                st.info("👉 New user? Register below →")
        
        with tab2:
            st.markdown("### Create Your Account")
            reg_username = st.text_input("Username", key="reg_user", placeholder="Choose a username")
            reg_email = st.text_input("Email", key="reg_email", placeholder="Your email")
            reg_password = st.text_input("Password", type="password", key="reg_pass", placeholder="Create password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Re-enter password")
            
            if st.button("🚀 Create Account", use_container_width=True, key="reg_btn"):
                if not all([reg_username, reg_email, reg_password, reg_confirm]):
                    st.error("❌ Please fill all fields!")
                elif reg_password != reg_confirm:
                    st.error("❌ Passwords don't match!")
                elif len(reg_password) < 6:
                    st.error("❌ Password must be at least 6 characters!")
                else:
                    st.session_state.user_logged_in = True
                    st.session_state.username = reg_username
                    st.success(f"✅ Account created! Welcome, {reg_username}!")
                    st.balloons()
                    st.rerun()

# ═══════════════════════════════════════════════════════════
# 2. SEMESTER SETUP PAGE (Enhanced)
# ═══════════════════════════════════════════════════════════

def show_semester_setup():
    """Setup semester with advanced features"""
    st.markdown("## 🚀 One-Click Semester Setup")
    st.markdown("*Create your semester and organize subjects instantly*")
    st.markdown("---")
    
    # Create new semester
    with st.form("semester_form", border=True):
        st.markdown("### 📚 Create New Semester")
        
        col1, col2 = st.columns(2)
        
        with col1:
            semester_name = st.text_input(
                "Semester Name",
                placeholder="e.g., Fall 2024, Semester 5",
                help="Give your semester a unique name"
            )
        
        with col2:
            semester_type = st.selectbox(
                "Semester Type",
                ["Regular", "Summer", "Winter", "Online"]
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "📅 Semester Start Date",
                value=datetime.now()
            )
        
        with col2:
            end_date = st.date_input(
                "📅 Semester End Date",
                value=datetime.now() + timedelta(days=120)
            )
        
        num_subjects = st.slider(
            "How many subjects in this semester?",
            min_value=1,
            max_value=10,
            value=5,
            help="Slide to select number of subjects"
        )
        
        submitted = st.form_submit_button("✅ Create Semester", use_container_width=True)
        
        if submitted:
            if semester_name:
                if end_date <= start_date:
                    st.error("❌ End date must be after start date!")
                else:
                    sem_id = str(uuid.uuid4())
                    st.session_state.semesters[sem_id] = {
                        'name': semester_name,
                        'type': semester_type,
                        'start_date': start_date,
                        'end_date': end_date,
                        'subjects': {},
                        'num_subjects': num_subjects,
                        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.current_semester = sem_id
                    st.success(f"✅ Semester '{semester_name}' created successfully!")
            else:
                st.error("❌ Please enter a semester name!")
    
    # Add subjects
    if st.session_state.current_semester:
        st.markdown("---")
        sem = st.session_state.semesters[st.session_state.current_semester]
        
        st.markdown(f"### 📖 Add Subjects to **{sem['name']}**")
        st.info(f"📝 Add up to {sem['num_subjects']} subjects")
        
        for i in range(sem['num_subjects']):
            with st.expander(f"Subject {i+1}", expanded=(i==0)):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    subject_name = st.text_input(
                        f"Subject Name",
                        placeholder="e.g., Advanced Mathematics",
                        key=f"subject_name_{i}"
                    )
                
                with col2:
                    subject_code = st.text_input(
                        f"Subject Code",
                        placeholder="e.g., MATH301",
                        key=f"subject_code_{i}"
                    )
                
                with col3:
                    credits = st.number_input(
                        f"Credits",
                        min_value=1,
                        max_value=5,
                        value=3,
                        key=f"credits_{i}"
                    )
                
                with col4:
                    professor = st.text_input(
                        f"Professor Name",
                        placeholder="Dr. Smith",
                        key=f"professor_{i}"
                    )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    exam_date = st.date_input(
                        f"📅 Exam Date",
                        value=sem['end_date'],
                        key=f"exam_date_{i}"
                    )
                
                with col2:
                    exam_type = st.selectbox(
                        f"Exam Type",
                        ["Written", "Practical", "Project", "Mixed"],
                        key=f"exam_type_{i}"
                    )
                
                if st.button(f"✅ Save Subject {i+1}", use_container_width=True, key=f"save_subject_{i}"):
                    if subject_name and subject_code:
                        subj_id = str(uuid.uuid4())
                        sem['subjects'][subj_id] = {
                            'name': subject_name,
                            'code': subject_code,
                            'credits': credits,
                            'professor': professor,
                            'exam_date': exam_date,
                            'exam_type': exam_type,
                            'files': [],
                            'notes': [],
                            'flashcards': [],
                            'tests': []
                        }
                        st.success(f"✅ {subject_name} added!")
                    else:
                        st.error("❌ Please fill subject name and code!")
        
        # Display saved subjects
        if sem['subjects']:
            st.markdown("---")
            st.markdown("### 📚 Your Subjects")
            
            cols = st.columns(len(sem['subjects']))
            for col, (subj_id, subject) in zip(cols, sem['subjects'].items()):
                with col:
                    with st.container(border=True):
                        st.markdown(f"### {subject['name']}")
                        st.caption(f"Code: {subject['code']}")
                        st.write(f"📚 Credits: {subject['credits']}")
                        st.write(f"👨‍🏫 Prof: {subject['professor']}")
                        
                        days_until = (subject['exam_date'] - datetime.now().date()).days
                        if days_until > 0:
                            st.warning(f"📅 Exam in {days_until} days")
                        else:
                            st.error("⏰ Exam today or passed!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Files", len(subject['files']))
                        with col2:
                            st.metric("Notes", len(subject['notes']))

# ═══════════════════════════════════════════════════════════
# 3. FILE ORGANIZER PAGE (Enhanced)
# ═══════════════════════════════════════════════════════════

def show_file_organizer():
    """Upload and organize study materials"""
    st.markdown("## 📂 Smart File Organizer")
    st.markdown("*Upload PDFs, presentations, and more*")
    st.markdown("---")
    
    if not st.session_state.current_semester:
        st.warning("⚠️ Please create a semester first!")
        return
    
    sem = st.session_state.semesters[st.session_state.current_semester]
    
    if not sem['subjects']:
        st.warning("⚠️ Please add subjects first!")
        return
    
    # Select subject
    subject_names = [f"{s['name']} ({s['code']})" for s in sem['subjects'].values()]
    selected_subject = st.selectbox("📚 Select Subject", subject_names)
    
    subject_id = list(sem['subjects'].keys())[subject_names.index(selected_subject)]
    subject = sem['subjects'][subject_id]
    
    st.markdown(f"### Organizing for **{subject['name']}**")
    
    # Upload files
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### 📤 Upload Study Materials")
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'pptx', 'txt', 'png', 'jpg', 'jpeg'],
            help="Upload documents, presentations, or images"
        )
    
    with col2:
        st.markdown("#### 🏷️ Tags")
        tags = st.text_input(
            "Tags (comma-separated)",
            placeholder="Chapter1, Important",
            help="Organize with tags"
        )
    
    file_type_select = st.radio("File Type:", ["Lecture", "Assignment", "Notes", "Reference"], horizontal=True)
    
    if uploaded_files and st.button("📤 Upload Files", use_container_width=True):
        for uploaded_file in uploaded_files:
            try:
                file_info = {
                    'id': str(uuid.uuid4()),
                    'name': uploaded_file.name,
                    'size': f"{uploaded_file.size / 1024:.2f} KB",
                    'uploaded_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'tags': tags,
                    'type': file_type_select,
                    'file_data': uploaded_file.read()  # Store file data
                }
                subject['files'].append(file_info)
                st.success(f"✅ Uploaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"❌ Error uploading {uploaded_file.name}: {str(e)}")
    
    # Display files
    if subject['files']:
        st.markdown("---")
        st.markdown("#### 📁 Your Files")
        
        for idx, file in enumerate(subject['files']):
            with st.container(border=True):
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"📄 **{file['name']}**")
                    st.caption(f"Type: {file['type']} | Size: {file['size']}")
                    if file['tags']:
                        st.caption(f"🏷️ Tags: {file['tags']}")
                
                with col2:
                    if st.button("👁️", key=f"view_{idx}", help="View content"):
                        st.info(f"Viewing: {file['name']}")
                
                with col3:
                    if st.button("📝", key=f"extract_{idx}", help="Extract text"):
                        # Extract text for AI features
                        file_ext = file['name'].split('.')[-1].lower()
                        try:
                            from io import BytesIO
                            file_obj = BytesIO(file['file_data'])
                            extracted_text = DocumentExtractor.extract_text(file_obj, file_ext)
                            st.session_state.current_file_content = extracted_text
                            st.success("✅ Content extracted!")
                            st.text_area("Extracted Content", extracted_text, height=200)
                        except:
                            st.error("Could not extract")
                
                with col4:
                    if st.button("🤖", key=f"ai_analyze_{idx}", help="AI Analysis"):
                        st.session_state.show_ai_analysis = True
                
                with col5:
                    if st.button("🗑️", key=f"delete_{idx}", help="Delete"):
                        subject['files'].pop(idx)
                        st.success("Deleted!")
                        st.rerun()
    else:
        st.info("📁 No files uploaded yet")

# ═══════════════════════════════════════════════════════════
# 4. AI CHAT ASSISTANT (New Premium Feature)
# ═══════════════════════════════════════════════════════════

def show_ai_chat_assistant():
    """AI-powered chat for questions and learning"""
    st.markdown("## 🤖 AI Study Chat Assistant")
    st.markdown("*Ask me anything about your studies!*")
    st.markdown("---")
    
    if not st.session_state.current_semester:
        st.warning("⚠️ Please create a semester first!")
        return
    
    sem = st.session_state.semesters[st.session_state.current_semester]
    
    if not sem['subjects']:
        st.warning("⚠️ Please add subjects first!")
        return
    
    # Select subject
    subject_names = [f"{s['name']} ({s['code']})" for s in sem['subjects'].values()]
    selected_subject = st.selectbox("📚 Select Subject for Chat", subject_names, key="chat_subject")
    
    subject_id = list(sem['subjects'].keys())[subject_names.index(selected_subject)]
    subject = sem['subjects'][subject_id]
    
    st.markdown(f"### Chatting about **{subject['name']}**")
    
    if not subject['files']:
        st.warning("📁 Please upload study materials first to use AI features!")
        return
    
    # Simulate AI features (without real API for basic version)
    st.markdown("#### What would you like to do?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Summarize My Materials", use_container_width=True):
            st.info("✨ Summarizing your uploaded materials...")
            # Simulated summary
            st.markdown("""
            **Key Points from Your Materials:**
            - Main concept 1: Clear explanation here
            - Main concept 2: Important details
            - Key takeaway: What you should remember
            """)
    
    with col2:
        if st.button("🎯 Explain a Concept", use_container_width=True):
            concept = st.text_input("What concept would you like explained?")
            if concept:
                st.info(f"✨ Explaining '{concept}' in simple terms...")
                st.markdown(f"""
                **Understanding {concept}:**
                
                Simple Explanation: {concept} is like...
                
                Key Points:
                - Point 1
                - Point 2
                - Point 3
                """)
    
    # Question input
    st.markdown("---")
    st.markdown("#### 💬 Ask Your Question")
    
    question = st.text_area(
        "Type your question here:",
        placeholder="What is...? How does...? Why...?",
        height=100
    )
    
    if st.button("🚀 Get Answer", use_container_width=True):
        if question:
            st.info("🤖 Thinking about your question...")
            # Simulated AI response
            st.markdown(f"""
            **Your Question:** {question}
            
            **AI Answer:**
            Based on your study materials, here's the answer:
            
            1. First key point
            2. Second explanation
            3. Important detail
            
            **Example:** ...
            
            **Remember:** This is an important concept for your exam!
            """)
        else:
            st.error("Please ask a question!")

# ═══════════════════════════════════════════════════════════
# 5. ADVANCED AI FEATURES (New)
# ═══════════════════════════════════════════════════════════

def show_ai_features():
    """Advanced AI features for studying"""
    st.markdown("## 🧠 Advanced AI Study Features")
    st.markdown("*Powered by AI for smarter learning*")
    st.markdown("---")
    
    if not st.session_state.current_semester:
        st.warning("⚠️ Please create a semester first!")
        return
    
    sem = st.session_state.semesters[st.session_state.current_semester]
    
    if not sem['subjects']:
        st.warning("⚠️ Please add subjects first!")
        return
    
    # Select subject
    subject_names = [f"{s['name']} ({s['code']})" for s in sem['subjects'].values()]
    selected_subject = st.selectbox("📚 Select Subject", subject_names, key="ai_subject")
    
    subject_id = list(sem['subjects'].keys())[subject_names.index(selected_subject)]
    subject = sem['subjects'][subject_id]
    
    if not subject['files']:
        st.warning("📁 Upload materials first!")
        return
    
    # Tabs for different AI features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Summarize",
        "🎓 Learn",
        "📚 Flashcards",
        "📖 Revision Notes",
        "❓ Q&A"
    ])
    
    with tab1:
        st.markdown("### 📝 Document Summarizer")
        summary_type = st.radio("Summary Type:", ["Short (5-7 points)", "Detailed"], horizontal=True)
        
        if st.button("Generate Summary", use_container_width=True):
            st.success("✅ Summary generated!")
            st.markdown("""
            **Summary of Your Materials:**
            
            1. **Main Concept:** Clear overview
            2. **Key Details:** Important information
            3. **Core Ideas:** Essential learning points
            4. **Applications:** Real-world usage
            5. **Key Takeaways:** What to remember
            """)
    
    with tab2:
        st.markdown("### 🎓 Concept Explainer")
        concept = st.text_input("Concept to explain:", placeholder="e.g., Photosynthesis")
        
        if st.button("Explain This", use_container_width=True):
            if concept:
                st.success(f"✅ Explaining '{concept}'!")
                st.markdown(f"""
                **Simple Explanation of {concept}:**
                
                **In Everyday Terms:** Think of it like...
                
                **Step-by-Step:**
                1. First, understand...
                2. Then, consider...
                3. Finally, remember...
                
                **Real Example:** ...
                
                **Common Mistakes to Avoid:**
                - ❌ Wrong idea 1
                - ❌ Wrong idea 2
                
                **Pro Tip:** 💡 Remember this when studying!
                """)
    
    with tab3:
        st.markdown("### 📚 Flashcard Generator")
        num_cards = st.slider("Number of flashcards:", 5, 30, 10)
        
        if st.button("Generate Flashcards", use_container_width=True):
            st.success(f"✅ Generated {num_cards} flashcards!")
            
            # Simulate flashcards
            for i in range(min(5, num_cards)):
                with st.expander(f"Flashcard {i+1}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Question Side:**")
                        st.write("What is the key concept?")
                    with col2:
                        st.markdown("**Answer Side:**")
                        st.write("The answer with detailed explanation...")
    
    with tab4:
        st.markdown("### 📖 Revision Notes")
        
        if st.button("Create Revision Notes", use_container_width=True):
            st.success("✅ Revision notes created!")
            st.markdown("""
            **Revision Notes for This Topic:**
            
            #### 🔑 Key Definitions
            - Term 1: Definition
            - Term 2: Definition
            
            #### 📌 Important Concepts
            - Concept 1: Explanation
            - Concept 2: Explanation
            
            #### 🧪 Key Formulas
            - Formula 1: Explanation
            - Formula 2: Explanation
            
            #### 💡 Quick Tips
            - Tip 1: Remember this
            - Tip 2: Don't forget this
            
            #### ⚠️ Common Mistakes
            - Mistake 1: How to avoid
            - Mistake 2: How to avoid
            """)
    
    with tab5:
        st.markdown("### ❓ Q&A System")
        user_question = st.text_area("Ask a question about this topic:", height=100)
        
        if st.button("Get Answer", use_container_width=True):
            if user_question:
                st.success("✅ Answer from AI Assistant!")
                st.markdown(f"""
                **Your Question:** {user_question}
                
                **Detailed Answer:**
                Here's a comprehensive answer based on your study materials...
                
                **Key Points:**
                1. Point 1
                2. Point 2
                3. Point 3
                
                **Example:** 
                Real-world application of this concept...
                
                **Related Topics to Review:**
                - Topic 1
                - Topic 2
                """)

# ═══════════════════════════════════════════════════════════
# 6. MOCK TEST GENERATOR (Enhanced)
# ═══════════════════════════════════════════════════════════

def show_mock_tests():
    """Generate and take AI-powered mock tests"""
    st.markdown("## 🧪 AI Mock Test Generator")
    st.markdown("*Generate tests with smart questions*")
    st.markdown("---")
    
    if not st.session_state.current_semester:
        st.warning("⚠️ Please create a semester first!")
        return
    
    sem = st.session_state.semesters[st.session_state.current_semester]
    
    if not sem['subjects']:
        st.warning("⚠️ Please add subjects first!")
        return
    
    # Select subject
    subject_names = [f"{s['name']} ({s['code']})" for s in sem['subjects'].values()]
    selected_subject = st.selectbox("📚 Select Subject for Test", subject_names, key="test_subject")
    
    subject_id = list(sem['subjects'].keys())[subject_names.index(selected_subject)]
    subject = sem['subjects'][subject_id]
    
    if not subject['files']:
        st.warning("📁 Upload study materials first to generate tests!")
        return
    
    st.markdown(f"### Generating Test for **{subject['name']}**")
    
    # Test customization
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_marks = st.selectbox(
            "📊 Total Marks",
            [20, 50, 75, 100],
            help="Select exam total marks"
        )
    
    with col2:
        num_questions = st.number_input(
            "❓ Number of Questions",
            min_value=5,
            max_value=50,
            value=10,
            help="How many questions?"
        )
    
    with col3:
        difficulty = st.selectbox(
            "📈 Difficulty",
            ["Easy", "Medium", "Hard"],
            help="Question difficulty level"
        )
    
    # Test format options
    st.markdown("#### 📋 Question Format")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mcq_count = st.number_input("MCQs:", 0, num_questions, int(num_questions*0.5))
    
    with col2:
        short_count = st.number_input("Short Answer:", 0, num_questions, int(num_questions*0.3))
    
    with col3:
        long_count = st.number_input("Long Answer:", 0, num_questions, int(num_questions*0.2))
    
    test_name = st.text_input(
        "📝 Test Name",
        placeholder="e.g., Chapter 5 Quiz, Midterm Practice",
        help="Give your test a name"
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        test_instructions = st.text_area(
            "📋 Test Instructions (Optional)",
            placeholder="e.g., 'Answer all questions. 1 hour time limit.'",
            height=60
        )
    
    with col2:
        time_limit = st.number_input(
            "⏱️ Time Limit (minutes)",
            min_value=15,
            max_value=240,
            value=60,
            help="Duration for the test"
        )
    
    if st.button("🚀 Generate Test", use_container_width=True):
        if test_name:
            with st.spinner("🤖 Generating AI-powered test..."):
                test_id = str(uuid.uuid4())
                test_data = {
                    'id': test_id,
                    'name': test_name,
                    'subject': subject['name'],
                    'total_marks': total_marks,
                    'num_questions': num_questions,
                    'difficulty': difficulty,
                    'format': f"{mcq_count} MCQs, {short_count} Short, {long_count} Long",
                    'time_limit': time_limit,
                    'instructions': test_instructions,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'questions': []
                }
                
                # Simulate test generation
                for i in range(1, min(num_questions + 1, 4)):
                    if i <= mcq_count:
                        test_data['questions'].append({
                            'number': i,
                            'type': 'MCQ',
                            'question': f'Question {i} from {subject["name"]}?',
                            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                            'answer': 'A'
                        })
                    elif i <= mcq_count + short_count:
                        test_data['questions'].append({
                            'number': i,
                            'type': 'Short Answer',
                            'question': f'Short answer question {i}?',
                            'max_words': 100
                        })
                    else:
                        test_data['questions'].append({
                            'number': i,
                            'type': 'Long Answer',
                            'question': f'Essay question {i}?',
                            'marks': 10
                        })
                
                st.session_state.mock_tests[test_id] = test_data
                
                st.success("✅ Test generated successfully!")
                st.markdown(f"""
                #### 📋 Test Created: {test_name}
                - **Total Marks:** {total_marks}
                - **Questions:** {num_questions}
                - **Difficulty:** {difficulty}
                - **Time Limit:** {time_limit} minutes
                - **Format:** {test_data['format']}
                """)
                
                # Show take test button
                st.markdown("---")
                if st.button("▶️ Take This Test Now", use_container_width=True):
                    st.session_state.current_test_id = test_id
                    st.rerun()
        else:
            st.error("❌ Please enter a test name!")
    
    # Display existing tests
    if st.session_state.mock_tests:
        st.markdown("---")
        st.markdown("### 📚 Your Mock Tests")
        
        for test_id, test in st.session_state.mock_tests.items():
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.markdown(f"### {test['name']}")
                    st.caption(f"Subject: {test['subject']} | Difficulty: {test['difficulty']}")
                
                with col2:
                    st.metric("Marks", test['total_marks'])
                
                with col3:
                    st.metric("Questions", test['num_questions'])
                
                with col4:
                    if st.button("▶️ Take", key=f"take_test_{test_id}"):
                        st.session_state.current_test_id = test_id
                        st.rerun()

# ═══════════════════════════════════════════════════════════
# 7. TAKE TEST PAGE
# ═══════════════════════════════════════════════════════════

def show_take_test():
    """Take a mock test"""
    if 'current_test_id' not in st.session_state:
        return
    
    test_id = st.session_state.current_test_id
    test = st.session_state.mock_tests.get(test_id)
    
    if not test:
        st.error("Test not found!")
        return
    
    st.markdown(f"## 📝 {test['name']}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Marks", test['total_marks'])
    with col2:
        st.metric("Questions", len(test['questions']))
    with col3:
        st.metric("Difficulty", test['difficulty'])
    with col4:
        st.metric("Time Limit", f"{test['time_limit']} min")
    
    st.markdown("---")
    
    # Test questions
    for q_idx, question in enumerate(test['questions']):
        st.markdown(f"### Question {q_idx + 1} ({question['type']})")
        st.write(question['question'])
        
        if question['type'] == 'MCQ':
            st.radio("Select answer:", question['options'], key=f"q_{question['number']}")
        elif question['type'] == 'Short Answer':
            st.text_area("Your answer:", height=80, key=f"q_short_{question['number']}")
        else:
            st.text_area("Your essay answer:", height=150, key=f"q_long_{question['number']}")
        
        st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Submit Test", use_container_width=True):
            st.success("✅ Test submitted!")
            st.markdown("""
            ### 📊 Test Results
            
            **Score:** 75 / 100 (75%)
            
            **Performance:** Excellent! 🎉
            
            **Analysis:**
            - MCQs: 10/10 ✅
            - Short Answer: 8/10 ✅
            - Long Answer: 7/10 ⚠️
            
            **Weak Areas:** Focus on long-answer questions
            
            **Recommended Review Topics:**
            - Topic 1
            - Topic 2
            """)
    
    with col2:
        if st.button("🚪 Exit Test", use_container_width=True):
            st.session_state.current_test_id = None
            st.rerun()

# ═══════════════════════════════════════════════════════════
# 8. PROGRESS DASHBOARD (Enhanced)
# ═══════════════════════════════════════════════════════════

def show_dashboard():
    """Smart progress tracking dashboard"""
    st.markdown("## 📊 Your Progress Dashboard")
    st.markdown("*Track your academic performance*")
    st.markdown("---")
    
    if not st.session_state.current_semester:
        st.warning("⚠️ Please create a semester first!")
        return
    
    sem = st.session_state.semesters[st.session_state.current_semester]
    
    # Statistics
    total_subjects = len(sem['subjects'])
    total_files = sum(len(s['files']) for s in sem['subjects'].values())
    total_tests = len(st.session_state.mock_tests)
    days_remaining = (sem['end_date'] - datetime.now().date()).days
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📚 Total Subjects",
            total_subjects,
            "Active courses"
        )
    
    with col2:
        st.metric(
            "📁 Study Materials",
            total_files,
            "Files uploaded"
        )
    
    with col3:
        st.metric(
            "🧪 Mock Tests",
            total_tests,
            "Tests generated"
        )
    
    with col4:
        st.metric(
            "⏳ Days Left",
            max(0, days_remaining),
            "Until end of semester"
        )
    
    st.markdown("---")
    
    # Subject-wise breakdown
    st.markdown("### 📚 Subjects Overview")
    
    if sem['subjects']:
        for subj_id, subject in sem['subjects'].items():
            with st.expander(f"📖 {subject['name']} ({subject['code']})"):
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Files", len(subject['files']))
                
                with col2:
                    st.metric("Notes", len(subject['notes']))
                
                with col3:
                    st.metric("Flashcards", len(subject['flashcards']))
                
                with col4:
                    st.metric("Tests", len(subject['tests']))
                
                with col5:
                    days_to_exam = (subject['exam_date'] - datetime.now().date()).days
                    if days_to_exam > 0:
                        st.metric("Days to Exam", days_to_exam)
                    else:
                        st.error("Exam completed!")
                
                # Progress bar
                st.progress(0.65, text="65% of material covered")
    
    st.markdown("---")
    
    # Study streak
    st.markdown("### 🔥 Study Streak")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Streak", "7 days", "Keep it up! 🎯")
    
    with col2:
        st.metric("Best Streak", "12 days", "You can do better!")
    
    with col3:
        st.metric("This Month", "120 hours", "Great effort!")
    
    st.markdown("---")
    
    # Upcoming exams
    st.markdown("### 📅 Upcoming Exams")
    
    exams_upcoming = []
    for subject in sem['subjects'].values():
        if subject['exam_date'] >= datetime.now().date():
            exams_upcoming.append(subject)
    
    if exams_upcoming:
        for subject in sorted(exams_upcoming, key=lambda x: x['exam_date']):
            days = (subject['exam_date'] - datetime.now().date()).days
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"📝 {subject['name']}")
            
            with col2:
                st.write(f"📅 {subject['exam_date'].strftime('%d %b')}")
            
            with col3:
                if days > 7:
                    st.success(f"{days} days left")
                elif days > 3:
                    st.warning(f"{days} days left")
                else:
                    st.error(f"{days} days left!")

# ═══════════════════════════════════════════════════════════
# 9. STUDY NOTES PAGE
# ═══════════════════════════════════════════════════════════

def show_study_notes():
    """Create and manage study notes"""
    st.markdown("## 📝 Study Notes")
    st.markdown("*Create rich, organized notes*")
    st.markdown("---")
    
    if not st.session_state.current_semester:
        st.warning("⚠️ Please create a semester first!")
        return
    
    sem = st.session_state.semesters[st.session_state.current_semester]
    
    if not sem['subjects']:
        st.warning("⚠️ Please add subjects first!")
        return
    
    # Create new note
    st.markdown("### ✍️ Create New Note")
    
    subject_names = [f"{s['name']} ({s['code']})" for s in sem['subjects'].values()]
    selected_subject = st.selectbox("📚 Select Subject", subject_names)
    
    subject_id = list(sem['subjects'].keys())[subject_names.index(selected_subject)]
    subject = sem['subjects'][subject_id]
    
    note_title = st.text_input("Note Title", placeholder="e.g., Chapter 5 Summary")
    note_content = st.text_area("Note Content", height=300, placeholder="Start typing your notes...")
    
    if st.button("💾 Save Note", use_container_width=True):
        if note_title and note_content:
            note = {
                'id': str(uuid.uuid4()),
                'title': note_title,
                'content': note_content,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            subject['notes'].append(note)
            st.success("✅ Note saved!")
        else:
            st.error("❌ Please fill in title and content!")
    
    # Display notes
    if subject['notes']:
        st.markdown("---")
        st.markdown("### 📖 Your Notes")
        
        for idx, note in enumerate(subject['notes']):
            with st.expander(f"📝 {note['title']}", expanded=(idx==0)):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.write(note['content'])
                    st.caption(f"Created: {note['created_at']}")
                
                with col2:
                    if st.button("🗑️", key=f"delete_note_{idx}"):
                        subject['notes'].pop(idx)
                        st.rerun()

# ═══════════════════════════════════════════════════════════
# 10. SETTINGS PAGE
# ═══════════════════════════════════════════════════════════

def show_settings():
    """User settings and preferences"""
    st.markdown("## ⚙️ Settings")
    st.markdown("*Customize your OCSS experience*")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🎨 Appearance", "🔔 Notifications"])
    
    with tab1:
        st.markdown("### User Profile")
        st.text_input("Username", value=st.session_state.username, disabled=True)
        st.text_input("Email", value="student@example.com")
        st.text_input("Phone", value="")
        
        if st.button("💾 Save Profile"):
            st.success("✅ Profile updated!")
    
    with tab2:
        st.markdown("### Appearance")
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        font_size = st.slider("Font Size", 10, 20, 14)
        
        if st.button("💾 Save Appearance"):
            st.success("✅ Appearance updated!")
    
    with tab3:
        st.markdown("### Notifications")
        st.checkbox("Email notifications", value=True)
        st.checkbox("Exam reminders", value=True)
        st.checkbox("Assignment reminders", value=True)
        st.checkbox("Study streak notifications", value=True)
        
        if st.button("💾 Save Notifications"):
            st.success("✅ Notification settings updated!")
    
    st.markdown("---")
    st.markdown("### Account")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔐 Change Password", use_container_width=True):
            st.info("Password change feature coming soon!")
    
    with col2:
        if st.button("🗑️ Delete Account", use_container_width=True):
            st.warning("Account deletion is permanent!")

# ═══════════════════════════════════════════════════════════
# MAIN APP LOGIC
# ═══════════════════════════════════════════════════════════

if not st.session_state.user_logged_in:
    show_login_page()

else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        
        if st.session_state.current_semester:
            sem_name = st.session_state.semesters[st.session_state.current_semester]['name']
            st.markdown(f"**Semester:** {sem_name}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    # Main navigation
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "📍 Navigation",
        [
            "📊 Dashboard",
            "🚀 Semester Setup",
            "📂 File Organizer",
            "🤖 AI Chat",
            "🧠 AI Features",
            "🧪 Mock Tests",
            "📝 Study Notes",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )
    
    # Page routing
    if page == "📊 Dashboard":
        show_dashboard()
    
    elif page == "🚀 Semester Setup":
        show_semester_setup()
    
    elif page == "📂 File Organizer":
        show_file_organizer()
    
    elif page == "🤖 AI Chat":
        show_ai_chat_assistant()
    
    elif page == "🧠 AI Features":
        show_ai_features()
    
    elif page == "🧪 Mock Tests":
        if 'current_test_id' in st.session_state and st.session_state.current_test_id:
            show_take_test()
        else:
            show_mock_tests()
    
    elif page == "📝 Study Notes":
        show_study_notes()
    
    elif page == "⚙️ Settings":
        show_settings()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 💡 Tips
    1. Upload study materials to unlock AI features
    2. Generate mock tests to practice
    3. Use the AI chat to clear doubts
    4. Track your progress on the dashboard
    5. Create notes for better retention
    """)
