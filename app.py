import streamlit as st
import os
import sys
import utils
import agents
import database

# 页面配置（必须放在最前面）
st.set_page_config(page_title="智能面试助手", page_icon="🎓", layout="wide")

# 全局初始化
sys.path.append(os.getcwd())
os.environ["PATH"] += os.pathsep + os.getcwd()

# ========== 智能跳转功能核心（必须放在所有组件渲染之前）==========
def smart_jump(user_input):
    """智能识别用户问题中的功能关键词，自动跳转到对应页面"""
    # 功能关键词映射表
    function_map = {
        "📄 简历评估": ["简历", "评估", "打分", "优化", "修改", "润色"],
        "🎙️ 面试录音分析": ["录音", "音频", "转写", "分析", "语音", "说话"],
        "❓ 个性化面试题": ["面试题", "题目", "出题", "练习题", "考题"],
        "🎯 实时面试模拟": ["面试", "模拟", "练习", "实战", "演练"],
        "✉️ 求职信生成": ["求职信", "自荐信", "cover letter", "申请信"],
        "💰 薪资谈判": ["薪资", "工资", "薪水", "谈判", "谈薪", "待遇"],
        "📈 职业规划": ["规划", "发展", "路线", "方向", "未来"],
        "🔍 简历ATS优化": ["ats", "筛选", "通过率", "系统", "关键词"],
        "🎭 多风格面试模拟": ["风格", "压力面", "hr面", "技术面", "面试官"],
        "📝 面试复盘": ["复盘", "总结", "回顾", "反思", "分析"]
    }
    
    user_input_lower = user_input.lower()
    
    for page_name, keywords in function_map.items():
        for keyword in keywords:
            if keyword in user_input_lower:
                # 直接修改session_state并立即rerun（在组件渲染前执行，不会报错）
                st.session_state.single_menu = page_name
                st.rerun()
                return True
    return False

# 处理快捷提问和用户输入的智能跳转
if "quick_question" in st.session_state and st.session_state.quick_question:
    user_in = st.session_state.quick_question
    st.session_state.quick_question = ""
    smart_jump(user_in)

# ===================== 全局样式 + 留白美化（最终优化版）=====================
st.markdown("""
<style>
/* 全局背景：多层渐变填充留白 */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4edf7 50%, #c3cfe2 100%);
    background-attachment: fixed;
    min-height: 100vh;
}

/* 主内容区：新增装饰性背景图案 */
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 0 !important;
    min-height: 95vh;
    background-image: 
        radial-gradient(circle at 15% 20%, rgba(25,118,210,0.08) 0%, transparent 35%),
        radial-gradient(circle at 85% 75%, rgba(66,165,245,0.08) 0%, transparent 35%),
        radial-gradient(circle at 50% 50%, rgba(100,181,246,0.05) 0%, transparent 50%);
    background-repeat: no-repeat;
    position: relative;
}

/* 固定装饰元素（填充留白，不影响交互） */
.main .block-container::before,
.main .block-container::after {
    content: "";
    position: fixed;
    width: 200px;
    height: 200px;
    opacity: 0.06;
    pointer-events: none;
    z-index: 0;
}
.main .block-container::before {
    top: 10%;
    left: 5%;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%231976D2' d='M50 0L61 35L100 35L68 57L79 91L50 70L21 91L32 57L0 35L39 35Z'/%3E%3C/svg%3E") no-repeat center;
    background-size: contain;
}
.main .block-container::after {
    bottom: 15%;
    right: 8%;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle fill='%2342A5F5' cx='50' cy='50' r='40'/%3E%3C/svg%3E") no-repeat center;
    background-size: contain;
}

/* 聊天容器：精准计算高度，消除多余留白 */
.chat-container {
    background-color: rgba(255,255,255,0.8);
    border-radius: 12px;
    padding: 1.2rem;
    overflow-y: auto;
    margin-bottom: 0 !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    position: relative;
    z-index: 1;
}

/* 聊天消息自动滚动到底部 */
.chat-container > div:last-child {
    scroll-margin-bottom: 20px;
}

/* 底部固定输入栏：紧凑布局，消除多余空间 */
.chat-input-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #f5f7fa 0%, #e4edf7 50%, #c3cfe2 100%);
    padding: 0.8rem 2rem;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.08);
    z-index: 999;
}

/* 卡片样式 */
.card {
    background-color: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    z-index: 1;
}
.card:hover {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    transform: translateY(-2px);
}

h1, h2, h3 {
    color: #1976D2;
    font-weight: 600;
}

.stButton > button {
    background-color: #1976D2;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    border: none;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background-color: #1565C0;
    box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
    transform: translateY(-1px);
}

.danger-btn > button {
    background-color: #fff5f5;
    color: #e53e3e;
    border: 1px solid #fed7d7;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-weight: 500;
    width: 100%;
}
.danger-btn > button:hover {
    background-color: #fed7d7;
    color: #c53030;
}

.confirm-btn > button {
    background-color: #1976D2;
    color: white;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    width: 100%;
    height: 100%;
}
.cancel-btn > button {
    background-color: #f7fafc;
    color: #4a5568;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    width: 100%;
    height: 100%;
}

.stFileUploader > div {
    border-radius: 10px;
    border: 2px dashed #1976D2;
    background-color: #f8faff;
}
.stFileUploader > div > div:nth-child(2) > span {
    visibility: hidden;
    position: relative;
}
.stFileUploader > div > div:nth-child(2) > span::after {
    content: "在这里拖放简历文件";
    visibility: visible;
    position: absolute;
    left: 0;
    top: 0;
}

.stStatus > div, .stExpander, .stMetric {
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    background: #fff;
}

.global-title {
    text-align: center;
    margin-bottom: 1.5rem;
    padding: 1.2rem;
    background: linear-gradient(135deg, #1976D2 0%, #42A5F5 100%);
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(25, 118, 210, 0.2);
    position: relative;
    z-index: 1;
}
.global-title h1 {
    color: white;
    margin-bottom: 0.3rem;
    font-size: 2.2rem;
}
.global-title p {
    color: rgba(255,255,255,0.9);
    font-size: 1rem;
    margin:0;
}

/* 当前模型显示样式 */
.current-model-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1976D2 0%, #42A5F5 100%);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

/* 空白引导提示样式 */
.guide-tip {
    margin-top: 3rem;
    padding: 1.2rem;
    text-align: center;
    color: #5a6a85;
    font-size: 1rem;
    background: rgba(255,255,255,0.7);
    border-radius: 10px;
    border: 1px dashed #b3c8e8;
    position: relative;
    z-index: 1;
}

/* 侧边栏样式 */
.st-emotion-cache-16txtl3 {
    padding-top: 1.5rem;
    background: linear-gradient(180deg, #ffffff 0%, #f0f7ff 100%);
}
.sidebar-group-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #666;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    padding-left: 0.5rem;
}
div[role="radiogroup"] label {
    padding: 0.6rem 0.8rem;
    border-radius:8px;
    cursor:pointer;
}
div[role="radiogroup"] label:hover {background:#e3f2fd;}
div[role="radiogroup"] input:checked + div {
    background:#e3f2fd;
    border-left:4px solid #1976D2;
    border-radius:0 8px 8px 0;
}
div[role="radiogroup"] input {display:none;}

/* 暗黑模式适配 */
@media (prefers-color-scheme: dark) {
    .stApp { background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%); color:#fff; }
    .st-emotion-cache-16txtl3 { background: linear-gradient(180deg,#1E1E1E 0%,#263238 100%); }
    .card,.stExpander,.stMetric { background:#2d2d2d; }
    .stFileUploader > div { background:#333; border-color:#64b5f6; }
    .guide-tip { background:rgba(50,50,50,0.6); color:#b0c4de; border-color:#445577; }
    .main .block-container::before, .main .block-container::after { opacity: 0.04; }
    .chat-container { background-color: rgba(40,40,40,0.8); }
    .chat-input-bar { background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%); }
}
</style>
""", unsafe_allow_html=True)

# 全局标题
st.markdown("""
<div class="global-title">
    <h1>🎓 第八届传智杯 · 智能面试助手</h1>
    <p>多Agent协同 | 多模型支持 | 参赛专用版</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏配置
st.sidebar.title("🎓 智能面试助手")
st.sidebar.divider()

st.sidebar.subheader("🔧 系统设置")
selected_model = st.sidebar.selectbox(
    "选择大模型",
    options=list(agents.MODEL_CONFIGS.keys()),
    index=0,
    help="智谱清言4-Flash速度最快，讯飞星火推理最强"
)

# ✅ 修复：只调用init_llm，不尝试访问任何内部属性
agents.init_llm(selected_model)
st.sidebar.success(f"✅ 已切换到：{selected_model}")

dark_mode = st.sidebar.checkbox("🌙 暗黑模式")
if dark_mode:
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%); color:#fff; }
    .st-emotion-cache-16txtl3 { background: linear-gradient(180deg,#1E1E1E 0%,#263238 100%); }
    .card,.stExpander,.stMetric { background:#2d2d2d; }
    .stFileUploader > div { background:#333; border-color:#64b5f6; }
    .guide-tip { background:rgba(50,50,50,0.6); color:#b0c4de; border-color:#445577; }
    .main .block-container::before, .main .block-container::after { opacity: 0.04; }
    .chat-container { background-color: rgba(40,40,40,0.8); }
    .chat-input-bar { background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%); }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.markdown('<div class="sidebar-group-title">🏠 基础功能</div>', unsafe_allow_html=True)
menu = st.sidebar.radio(
    "",
    [
        "🏠 首页",
        "🤖 智能面试助手",
        "📄 简历评估",
        "🎙️ 面试录音分析",
        "❓ 个性化面试题",
        "🎯 实时面试模拟",
        "---",
        "✉️ 求职信生成",
        "💰 薪资谈判",
        "📈 职业规划",
        "🔍 简历ATS优化",
        "🎭 多风格面试模拟",
        "📝 面试复盘"
    ],
    index=0,
    label_visibility="collapsed",
    key="single_menu"
)
if menu == "---":
    st.stop()

st.sidebar.markdown("""
<style>
div[role="radiogroup"] label:nth-child(7) { display:none !important; }
div[role="radiogroup"] label:nth-child(6)::after {
    content:"";display:block;height:1px;background:#e0e0e0;margin:1rem 0.5rem;
}
div[role="radiogroup"] label:nth-child(7)::before {
    content:"✨ 扩展功能";display:block;font-size:0.85rem;color:#666;margin:1rem 0 0.5rem 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# 清除历史函数
def clear_history(table_name, display_name):
    if f"confirm_clear_{table_name}" not in st.session_state:
        st.session_state[f"confirm_clear_{table_name}"] = False
    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
    if st.button(f"🗑️ 清除{display_name}历史", key=f"clear_{table_name}"):
        st.session_state[f"confirm_clear_{table_name}"] = True
    if st.session_state[f"confirm_clear_{table_name}"]:
        st.warning(f"⚠️ 确定清除全部{display_name}记录？操作不可恢复！")
        c1,c2=st.columns(2)
        with c1:
            st.markdown('<div class="confirm-btn">',unsafe_allow_html=True)
            if st.button("✅ 确认清除",type="primary"):
                conn=database.get_conn()
                conn.execute(f"DELETE FROM {table_name}")
                conn.commit()
                conn.close()
                st.success("清除完成")
                st.session_state[f"confirm_clear_{table_name}"]=False
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="cancel-btn">',unsafe_allow_html=True)
            if st.button("❌ 取消"):
                st.session_state[f"confirm_clear_{table_name}"]=False
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ========== 页面内容 ==========
if menu == "🏠 首页":
    st.success("✅ 项目启动成功！所有功能正常运行")
    st.markdown("## 🎯 项目核心功能")
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown("""<div class="card"><h3 style="color:#1976D2;margin:0">📄 简历智能评估</h3><p>解析简历、违禁词检测、多维度评分+优化建议</p></div>""",unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card"><h3 style="color:#1976D2;margin:0">🎙️ 面试录音分析</h3><p>语音转写、回答点评、逻辑梳理+改进方向</p></div>""",unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card"><h3 style="color:#1976D2;margin:0">❓ 个性化面试题</h3><p>依托简历自动出题，配套答题参考要点</p></div>""",unsafe_allow_html=True)
    
    # 技术栈排版优化
    st.markdown("## 🛠️ 技术栈详情")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color:#1976D2;margin:0 0 1rem 0;">前端与核心框架</h3>
            <table style="width:100%;border-collapse:collapse;">
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:0.5rem 0;">前端框架</td>
                    <td style="padding:0.5rem 0;text-align:right;">Streamlit 1.35.0</td>
                </tr>
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:0.5rem 0;">大模型支持</td>
                    <td style="padding:0.5rem 0;text-align:right;">智谱/星火/通义/豆包</td>
                </tr>
                <tr>
                    <td style="padding:0.5rem 0;">文档解析</td>
                    <td style="padding:0.5rem 0;text-align:right;">PyPDF2 / python-docx</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color:#1976D2;margin:0 0 1rem 0;">辅助与数据模块</h3>
            <table style="width:100%;border-collapse:collapse;">
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:0.5rem 0;">语音转写</td>
                    <td style="padding:0.5rem 0;text-align:right;">OpenAI Whisper</td>
                </tr>
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:0.5rem 0;">数据存储</td>
                    <td style="padding:0.5rem 0;text-align:right;">SQLite 数据库</td>
                </tr>
                <tr>
                    <td style="padding:0.5rem 0;">架构模式</td>
                    <td style="padding:0.5rem 0;text-align:right;">多Agent协同架构</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="guide-tip">💡 左侧菜单栏选择对应功能，即可开始面试辅助操作</div>',unsafe_allow_html=True)

elif menu == "📄 简历评估":
    st.subheader("📄 简历智能评估")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        file=st.file_uploader("上传简历（PDF/DOCX）",type=["pdf","docx"])
        if file and st.button("🚀 开始评估"):
            os.makedirs("uploads/resumes",exist_ok=True)
            path=f"uploads/resumes/{file.name}"
            with open(path,"wb") as f:f.write(file.getbuffer())
            try:
                with st.status("评估解析中...") as status:
                    content=utils.parse_resume(path)
                    utils.check_forbidden(content)
                    res=agents.resume_agent.run(path,file.name)
                    status.update(label="✅ 评估完成",state="complete")
                col1,col2=st.columns([1,2])
                with col1:
                    st.metric("简历评分",f"{res['score']}分")
                    st.metric("模板相似度",f"{res['similarity']:.2%}")
                with col2:
                    st.markdown("### 评估报告")
                    st.markdown(res["report"])
                    st.download_button("下载报告",res["report"],"简历评估报告.txt")
            except Exception as e:
                st.error(f"评估失败：{e}")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    h1,h2=st.columns([8,2])
    with h1:st.subheader("📜 最近评估记录")
    with h2:clear_history("resumes","简历评估")
    conn=database.get_conn()
    rec=conn.execute("SELECT filename,score,report FROM resumes ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    if rec:
        for r in rec:
            with st.expander(f"{r['filename']} - {r['score']}分"):
                st.markdown(r["report"])
    else:
        st.info("暂无历史记录")
    st.markdown('<div class="guide-tip">📌 上传简历文件后点击评估，即可获取专业打分与优化意见</div>',unsafe_allow_html=True)

elif menu == "🎙️ 面试录音分析":
    st.subheader("🎙️ 面试录音分析")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        file=st.file_uploader("上传录音（MP3/WAV）",type=["mp3","wav"])
        if file and st.button("🎙️ 开始分析"):
            os.makedirs("uploads/audio",exist_ok=True)
            safe_name="".join([c for c in file.name if c.isalnum() or c in (".","_","-")])
            path=os.path.join("uploads","audio",safe_name)
            with open(path,"wb") as f:f.write(file.getbuffer())
            try:
                with st.status("语音解析分析中...") as status:
                    utils.init_whisper()
                    text=utils.audio_to_text(path)
                    res=agents.audio_agent.run(path,safe_name)
                    status.update(label="✅ 分析完成",state="complete")
                c1,c2=st.columns([1,2])
                with c1:
                    st.metric("面试评分",f"{res['score']}分")
                    st.download_button("下载转写文本",res["transcript"],f"{safe_name}_文本.txt")
                with c2:
                    st.markdown("录音转写内容")
                    st.text_area("",res["transcript"],height=120)
                    st.markdown("分析报告")
                    st.markdown(res["report"])
            except Exception as e:
                st.error(f"分析失败：{e}")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    h1,h2=st.columns([8,2])
    with h1:st.subheader("📜 最近分析记录")
    with h2:clear_history("interviews","录音分析")
    conn=database.get_conn()
    rec=conn.execute("SELECT filename,score,transcript,report FROM interviews ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    if rec:
        for r in rec:
            with st.expander(f"{r['filename']} - {r['score']}分"):
                st.text_area("转写",r["transcript"],height=80)
                st.markdown(r["report"])
    else:
        st.info("暂无历史记录")
    st.markdown('<div class="guide-tip">🎧 上传面试录音，自动转写文字并点评答题表现</div>',unsafe_allow_html=True)

elif menu == "❓ 个性化面试题":
    st.subheader("❓ 个性化面试题生成")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        file=st.file_uploader("上传简历生成题目",type=["pdf","docx"])
        if file and st.button("📝 生成面试题"):
            os.makedirs("uploads/resumes",exist_ok=True)
            path=f"uploads/resumes/{file.name}"
            with open(path,"wb") as f:f.write(file.getbuffer())
            try:
                with st.status("题目生成中..."):
                    content=utils.parse_resume(path)
                    res=agents.question_agent.run(content,file.name)
                st.markdown("### 面试练习题")
                st.markdown(res)
                st.download_button("下载题库",res,"面试题目.txt")
            except Exception as e:
                st.error(f"生成失败：{e}")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    h1,h2=st.columns([8,2])
    with h1:st.subheader("📜 最近生成记录")
    with h2:clear_history("generated_questions","面试题生成")
    conn=database.get_conn()
    rec=conn.execute("SELECT resume_filename,questions FROM generated_questions ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    if rec:
        for r in rec:
            with st.expander(r["resume_filename"]):
                st.markdown(r["questions"])
    else:
        st.info("暂无记录")
    st.markdown('<div class="guide-tip">📖 依托个人简历，定制专属岗位面试考题辅助备考</div>',unsafe_allow_html=True)

elif menu == "🎯 实时面试模拟":
    st.subheader("🎯 实时交互式面试模拟")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        if "interview_started" not in st.session_state:
            st.session_state.interview_started=False
            st.session_state.current_question=""
            st.session_state.feedback=""
            st.session_state.finished=False
        file=st.file_uploader("上传简历开始面试",type=["pdf","docx"])
        if file and not st.session_state.interview_started:
            if st.button("🚀 开始面试"):
                path=f"uploads/resumes/{file.name}"
                os.makedirs("uploads/resumes",exist_ok=True)
                with open(path,"wb") as f:f.write(file.getbuffer())
                content=utils.parse_resume(path)
                st.session_state.current_question=agents.interview_agent.start(content,file.name)
                st.session_state.interview_started=True
                st.rerun()
        if st.session_state.interview_started:
            st.markdown(f"### 面试官：{st.session_state.current_question}")
            ans=st.text_area("你的回答：",height=140)
            if st.button("✅ 提交回答") and ans:
                feed,next_q,fin=agents.interview_agent.answer(ans)
                st.session_state.feedback=feed
                st.session_state.finished=fin
                if not fin:
                    st.session_state.current_question=next_q
                else:
                    st.session_state.final_report=next_q
                st.rerun()
            if st.session_state.feedback:
                st.info("AI点评："+st.session_state.feedback)
            if st.session_state.finished:
                st.success("面试结束")
                st.markdown(st.session_state.final_report)
                st.download_button("下载面试报告",st.session_state.final_report,"模拟面试报告.txt")
                if st.button("🔄 重新开始"):
                    st.session_state.interview_started=False
                    st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="guide-tip">🤝 沉浸式模拟面试流程，实时收获答题点评与改进建议</div>',unsafe_allow_html=True)

elif menu == "✉️ 求职信生成":
    st.subheader("✉️ 专业求职信生成")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        job=st.text_input("目标岗位",placeholder="例如：Python开发工程师")
        company=st.text_input("目标公司",placeholder="例如：科技有限公司")
        file=st.file_uploader("上传简历",type=["pdf","docx"])
        if job and company and file and st.button("✉️ 生成求职信"):
            path=f"uploads/resumes/{file.name}"
            os.makedirs("uploads/resumes",exist_ok=True)
            with open(path,"wb") as f:f.write(file.getbuffer())
            content=utils.parse_resume(path)
            res=agents.cover_agent.run(content,job,company,file.name)
            st.markdown("### 求职信内容")
            st.markdown(res)
            st.download_button("下载文档",res,"求职信.txt")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    h1,h2=st.columns([8,2])
    with h1:st.subheader("历史生成记录")
    with h2:clear_history("cover_letters","求职信")
    key=st.text_input("搜索岗位/公司")
    conn=database.get_conn()
    if key:
        rec=conn.execute("SELECT job,company,content FROM cover_letters WHERE job LIKE ? OR company LIKE ?",(f"%{key}%",f"%{key}%")).fetchall()
    else:
        rec=conn.execute("SELECT job,company,content FROM cover_letters ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    for r in rec:
        with st.expander(f"{r['job']} | {r['company']}"):
            st.markdown(r["content"])
    st.markdown('<div class="guide-tip">📩 填写岗位与企业信息，快速生成贴合个人经历的求职自荐信</div>',unsafe_allow_html=True)

elif menu == "💰 薪资谈判":
    st.subheader("💰 薪资谈判助手")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        job=st.text_input("应聘岗位",placeholder="例如：后端开发")
        city=st.text_input("工作城市",placeholder="例如：广州")
        exp=st.number_input("工作经验（年）",0,20)
        if st.button("💰 获取薪资建议"):
            res=agents.salary_agent.run(job,city,exp)
            st.markdown("### 薪资参考与谈判话术")
            st.markdown(res)
            st.download_button("保存建议",res,"薪资谈判建议.txt")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    h1,h2=st.columns([8,2])
    with h1:st.subheader("查询记录")
    with h2:clear_history("salary_advice","薪资谈判")
    key=st.text_input("搜索岗位/城市")
    conn=database.get_conn()
    rec=conn.execute("SELECT job,city,experience,content FROM salary_advice ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    for r in rec:
        with st.expander(f"{r['job']} {r['city']} {r['experience']}年"):
            st.markdown(r["content"])
    st.markdown('<div class="guide-tip">💸 结合城市、岗位、工龄，给到合理薪资范围与谈判技巧</div>',unsafe_allow_html=True)

elif menu == "📈 职业规划":
    st.subheader("📈 个性化职业规划")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        interest=st.text_input("个人兴趣方向",placeholder="人工智能、前端、测试等")
        file=st.file_uploader("上传简历",type=["pdf","docx"])
        if interest and file and st.button("📈 生成职业规划"):
            path=f"uploads/resumes/{file.name}"
            os.makedirs("uploads/resumes",exist_ok=True)
            with open(path,"wb") as f:f.write(file.getbuffer())
            content=utils.parse_resume(path)
            res=agents.career_agent.run(content,interest,file.name)
            st.markdown("### 职业规划方案")
            st.markdown(res)
            st.download_button("下载方案",res,"职业规划.txt")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="guide-tip">🗺️ 结合自身履历与兴趣，制定短期中长期成长路线</div>',unsafe_allow_html=True)

elif menu == "🔍 简历ATS优化":
    st.subheader("🔍 简历ATS智能优化")
    st.markdown("自动检测ATS兼容问题，补齐岗位关键词优化简历通过率")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            file=st.file_uploader("上传简历",type=["pdf","docx"])
        with c2:
            jd=st.text_area("粘贴岗位JD描述",height=140)
        if file and jd and st.button("🚀 开始ATS优化"):
            path=f"uploads/resumes/{file.name}"
            with open(path,"wb") as f:f.write(file.getbuffer())
            content=utils.parse_resume(path)
            res=agents.ats_agent.run(content,file.name,jd)
            st.metric("ATS预估通过率",f"{res['score']}分")
            st.markdown("优化报告")
            st.markdown(res["report"])
            st.download_button("下载报告",res["report"],"ATS优化报告.txt")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="guide-tip">✅ 对标招聘要求整改简历，提升系统筛选通过率</div>',unsafe_allow_html=True)

elif menu == "🎭 多风格面试模拟":
    st.subheader("🎭 多风格面试官模拟")
    st.markdown("温和HR、压力面试、技术面三种模式随心练习")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        if "multi_interview_started" not in st.session_state:
            st.session_state.multi_interview_started=False
        file=st.file_uploader("上传简历开启模拟面试",type=["pdf","docx"])
        style=st.radio("选择面试风格",["温和HR面","严厉压力面","技术大牛面"],horizontal=True)
        if file and not st.session_state.multi_interview_started and st.button("🚀 开始面试"):
            path=f"uploads/resumes/{file.name}"
            with open(path,"wb") as f:f.write(file.getbuffer())
            content=utils.parse_resume(path)
            st.session_state.current_question=agents.multi_style_agent.start(content,file.name,style)
            st.session_state.multi_interview_started=True
            st.rerun()
        if st.session_state.multi_interview_started:
            st.markdown(f"面试官提问：{st.session_state.current_question}")
            ans=st.text_area("作答区域",height=140)
            if st.button("提交回答") and ans:
                resp,fin=agents.multi_style_agent.answer(ans)
                st.session_state.current_question=resp
                st.session_state.finished=fin
                st.rerun()
            if st.session_state.finished:
                st.success("面试结束")
                rep=agents.multi_style_agent.get_final_report()
                st.markdown(rep)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="guide-tip">🎬 模拟不同面试官风格，全方位锻炼临场应答能力</div>',unsafe_allow_html=True)

elif menu == "📝 面试复盘":
    st.subheader("📝 结构化面试复盘")
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        talk=st.text_area("粘贴完整面试对话记录",height=280,placeholder="面试官：xxx\n你：xxx")
        if talk and st.button("🚀 生成复盘报告"):
            rep=agents.review_agent.run(talk)
            st.markdown("### 面试复盘分析")
            st.markdown(rep)
            st.download_button("保存复盘",rep,"面试复盘报告.txt")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="guide-tip">📋 录入对话内容，客观分析优缺点并给出改进方向</div>',unsafe_allow_html=True)

elif menu == "🤖 智能面试助手":
    # 页面标题区域（紧凑布局）
    st.markdown("""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h2 style="color: #1976D2; margin-bottom: 0.5rem; font-size: 1.8rem;">🤖 智能面试助手</h2>
        <p style="color: #5a6a85; font-size: 1rem; margin: 0;">自然对话交互，一站式解决各类面试相关问题</p>
    </div>
    """, unsafe_allow_html=True)

    # ✅ 当前模型显示标识（直接使用侧边栏的selected_model变量，准确无误）
    st.markdown(f'<div class="current-model-badge">🔄 当前模型：{selected_model}</div>', unsafe_allow_html=True)

    # 功能介绍卡片（填充留白，提升体验）
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(25,118,210,0.1);">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📄</div>
            <div style="font-weight: 600; color: #1976D2; margin-bottom: 0.3rem;">简历相关</div>
            <div style="font-size: 0.85rem; color: #5a6a85;">简历评估、ATS优化、求职信生成</div>
        </div>
        <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(76,175,80,0.1);">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-weight: 600; color: #2e7d32; margin-bottom: 0.3rem;">面试练习</div>
            <div style="font-size: 0.85rem; color: #5a6a85;">面试模拟、多风格面试、录音分析</div>
        </div>
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(255,152,0,0.1);">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">💡</div>
            <div style="font-weight: 600; color: #ef6c00; margin-bottom: 0.3rem;">求职指导</div>
            <div style="font-size: 0.85rem; color: #5a6a85;">薪资谈判、职业规划、面试技巧</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 快捷提问按钮（一键提问，提升交互）
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <p style="color: #5a6a85; font-size: 0.9rem; margin-bottom: 0.8rem;">💬 试试这些问题：</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("帮我评估简历", use_container_width=True):
            st.session_state.quick_question = "帮我评估简历"
            st.rerun()
    with col2:
        if st.button("生成面试题", use_container_width=True):
            st.session_state.quick_question = "生成面试题"
            st.rerun()
    with col3:
        if st.button("如何回答优缺点", use_container_width=True):
            st.session_state.quick_question = "如何回答优缺点"
            st.rerun()
    with col4:
        if st.button("薪资谈判技巧", use_container_width=True):
            st.session_state.quick_question = "薪资谈判技巧"
            st.rerun()

    # 聊天容器（调整高度，合理分配空间）
    st.markdown('<div class="chat-container" style="min-height: calc(100vh - 450px); max-height: calc(100vh - 450px); margin-top: 1rem;">', unsafe_allow_html=True)
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # 显示所有聊天历史
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部固定输入栏
    st.markdown('<div class="chat-input-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns([9, 1])
    with col1:
        user_in = st.chat_input("输入你的面试问题")
    with col2:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 处理用户输入
    if user_in:
        # 先执行智能跳转检测
        if not smart_jump(user_in):
            # 如果没有匹配到功能，使用统一助手的公开方法生成回复
            st.session_state.chat_messages.append({"role": "user", "content": user_in})
            with st.chat_message("user"):
                st.markdown(user_in)
            with st.chat_message("assistant"):
                # ✅ 只使用公开的generate_response方法，不访问任何内部属性
                resp = agents.unified_assistant.generate_response(user_in)
                st.markdown(resp)
                st.session_state.chat_messages.append({"role": "assistant", "content": resp})
            # 自动滚动到底部
            st.html("""
            <script>
            setTimeout(() => {
                const chatContainer = document.querySelector('.chat-container');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }, 100);
            </script>
            """)