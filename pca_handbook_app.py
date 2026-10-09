import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

st.set_page_config(
    page_title="PCA Handbook",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b1f36;
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #061424;
        color: #ffffff;
    }
    .main-header {
        font-size: 2.3rem;
        color: #00d2ff;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #cbd5e1;
        margin-bottom: 1.5rem;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #f8fafc;
    }
    [data-testid="stSidebar"] label {
        color: #f8fafc !important;
        font-weight: 500;
    }
    .neon-highlight {
        background-color: rgba(0, 255, 102, 0.15);
        border-left: 5px solid #00FF66;
        padding: 10px;
        margin: 5px 0;
        border-radius: 4px;
        color: #00FF66 !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HÀM HỖ TRỢ QUẢN LÝ BẢNG DỮ LIỆU CSV
# ---------------------------------------------------------
def load_table_data(filename, default_data):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            if not df.empty:
                return df
        except Exception:
            pass
    df_default = pd.DataFrame(default_data)
    df_default.to_csv(filename, index=False)
    return df_default

def save_table_data(filename, df):
    df.to_csv(filename, index=False)

# ---------------------------------------------------------
# HÀM HIỂN THỊ TRỰC TIẾP FILE PDF TRÊN STREAMLIT
# ---------------------------------------------------------
def render_file_preview_section(file_path, row, section_name, idx):
    file_ext = str(row['File Type']).lower()
    
    if os.path.exists(file_path):
        if file_ext == 'pdf':
            st.markdown(f"📄 **Xem trước trực tiếp tài liệu PDF: {row['File Name']}**")
            
            try:
                with open(file_path, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                
                # Nhúng trực tiếp bằng thẻ embed của HTML5, hỗ trợ trình đọc PDF tích hợp của Chrome/Edge
                pdf_display = f'''
                <embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf">
                '''
                st.markdown(pdf_display, unsafe_allow_html=True)
                
            except Exception as e:
                st.warning("⚠️ Không thể render trực tiếp khung PDF trên trình duyệt này.")
                
            # Cung cấp thêm nút tải dự phòng bên dưới
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="⬇ Tải file PDF về máy",
                data=pdf_bytes,
                file_name=row['File Name'],
                mime="application/pdf",
                key=f"fallback_dl_{section_name}_{idx}"
            )
                
        elif file_ext in ['png', 'jpg', 'jpeg']:
            st.image(file_path, caption=row['File Name'], use_container_width=True)
            
        elif file_ext in ['xlsx', 'xls']:
            try:
                df_excel = pd.read_excel(file_path)
                st.markdown(f"**📊 Xem trước dữ liệu Excel:**")
                st.dataframe(df_excel, use_container_width=True, height=300)
            except Exception as e:
                st.error(f"Không thể đọc file Excel: {e}")
                
        elif file_ext in ['txt', 'csv']:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            st.text_area("Nội dung file:", content, height=250, key=f"txt_content_{section_name}_{idx}")
        else:
            st.warning("⚠️ Định dạng file này không hỗ trợ xem trước trực tiếp.")
    else:
        st.error("❌ Không tìm thấy file vật lý trên máy này.")

# ---------------------------------------------------------
# HÀM QUẢN LÝ THƯ VIỆN TÀI LIỆU (DOCUMENT LIBRARY + PREVIEW)
# ---------------------------------------------------------
def render_doc_library(section_name):
    st.markdown(f'<div class="main-header">Document Library: {section_name}</div>', unsafe_allow_html=True)
    
    upload_dir = f"uploads_{section_name.lower()}"
    os.makedirs(upload_dir, exist_ok=True)
    meta_csv = f"metadata_{section_name.lower()}.csv"
    
    if os.path.exists(meta_csv):
        try:
            df_meta = pd.read_csv(meta_csv)
        except Exception:
            df_meta = pd.DataFrame(columns=["File Name", "Original Name", "Uploader", "Upload Date", "Description", "File Type"])
    else:
        df_meta = pd.DataFrame(columns=["File Name", "Original Name", "Uploader", "Upload Date", "Description", "File Type"])
        
    # --- FORM UPLOAD FILE MỚI ---
    with st.expander("📤 Upload tài liệu mới (Word, Excel, PPT, PDF, Ảnh...)", expanded=False):
        with st.form(key=f"upload_form_{section_name}", clear_on_submit=True):
            uploaded_file = st.file_uploader("Chọn file tài liệu:", type=["pdf", "docx", "doc", "xlsx", "xls", "pptx", "ppt", "txt", "png", "jpg", "jpeg"])
            uploader_name = st.text_input("Tên người upload (Uploader):", value="Admin")
            description = st.text_area("Mô tả nội dung tài liệu:")
            
            submitted = st.form_submit_button("Tải lên và Lưu")
            if submitted and uploaded_file is not None:
                file_path = os.path.join(upload_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                new_row = {
                    "File Name": uploaded_file.name,
                    "Original Name": uploaded_file.name,
                    "Uploader": uploader_name,
                    "Upload Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Description": description,
                    "File Type": uploaded_file.name.split('.')[-1].upper()
                }
                
                df_meta = pd.concat([df_meta, pd.DataFrame([new_row])], ignore_index=True)
                df_meta.to_csv(meta_csv, index=False)
                st.success(f"✅ Đã upload thành công file: {uploaded_file.name}")
                st.rerun()

    st.markdown("---")
    st.markdown("### 📚 Thư viện tài liệu hiện có")
    
    if df_meta.empty:
        st.info("ℹ Chưa có tài liệu nào được tải lên trong mục này.")
    else:
        for idx, row in df_meta.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 2, 1])
                with col1:
                    st.markdown(f"**📄 {row['File Name']}**")
                    if pd.notna(row['Description']) and str(row['Description']).strip() != "":
                        st.caption(f"Mô tả: {row['Description']}")
                with col2:
                    st.text(f"👤 {row['Uploader']}")
                with col3:
                    st.text(f"📅 {row['Upload Date']}")
                with col4:
                    file_path = os.path.join(upload_dir, row['File Name'])
                    file_ext = str(row['File Type']).lower()
                    
                    if file_ext in ['pdf', 'png', 'jpg', 'jpeg']:
                        if st.button("👁 Xem", key=f"preview_{section_name}_{idx}"):
                            st.session_state[f"show_preview_{section_name}_{idx}"] = not st.session_state.get(f"show_preview_{section_name}_{idx}", False)
                    
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="⬇ Tải",
                                data=f,
                                file_name=row['File Name'],
                                key=f"download_{section_name}_{idx}"
                            )
                with col5:
                    if st.button("🗑 Xóa", key=f"delete_{section_name}_{idx}"):
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        df_meta = df_meta.drop(idx).reset_index(drop=True)
                        df_meta.to_csv(meta_csv, index=False)
                        st.success("Đã xóa file thành công!")
                        st.rerun()
                
                # Gọi hàm xem trước đã được định nghĩa ở phía trên
                if st.session_state.get(f"show_preview_{section_name}_{idx}", False):
                    with st.expander(f"🔎 Xem trước tài liệu: {row['File Name']}", expanded=True):
                        render_file_preview_section(file_path, row, section_name, idx)
                
                st.divider()
# ---------------------------------------------------------
# THANH ĐIỀU HƯỚNG SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("📚 PCA Handbook")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Danh mục chính:",
    [
        "Trang chủ & Giới thiệu", 
        "PCA Systems (Chi tiết)",
        "Kiến thức chung", 
        "Cantilever", 
        "Vertical", 
        "Hokko", 
        "PCA Productivity",
        "Tài liệu & Tra cứu"
    ]
)

def render_sub_menu(category_name, options):
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"📁 **Thư mục con ({category_name}):**")
    sub_choice = st.sidebar.radio(
        "Chọn nội dung:",
        options,
        key=f"sub_{category_name}"
    )
    return sub_choice

sub_menu = None
if menu in ["Cantilever", "Vertical", "Hokko"]:
    sub_menu = render_sub_menu(menu, [
        "1. Thiết bị & Hình ảnh",
        "2. Flowchart (Quy trình)",
        "3. WI (Work Instruction)",
        "4. DOC (Tài liệu)",
        "5. Special Note (Lưu ý đặc biệt)"
    ])
elif menu == "PCA Productivity":
    sub_menu = render_sub_menu(menu, [
        "PCA Cant Productivity",
        "PCA Vert Productivity"
    ])

st.sidebar.markdown("---")
st.sidebar.info("📌 **Phiên bản:** 1.0.0 \n📅 **Cập nhật:** 2026 \n🏢 **PCA Department**")

# ---------------------------------------------------------
# NỘI DUNG CÁC TRANG
# ---------------------------------------------------------

if menu == "Trang chủ & Giới thiệu":
    st.markdown('<div class="main-header">PCA Technical Handbook</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Tài liệu hướng dẫn kỹ thuật và thông tin sản phẩm chuẩn hóa nội bộ</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🏗️ PCA Systems")
        st.write("Hệ thống các dòng máy và giải cấu trúc tiêu chuẩn PCA.")
    with col2:
        st.markdown("### ↕ Vertical")
        st.write("Giải pháp lưu trữ dạng đứng, tối ưu diện tích mặt bằng.")
    with col3:
        st.markdown("### ⚙️ Hokko")
        st.write("Dòng sản phẩm cơ khí chính xác, linh kiện lắp ráp nhanh.")

# 1.1. PCA SYSTEMS CHI TIẾT (CÓ CHỌN VÀ HIỆN ẢNH)
elif menu == "PCA Systems (Chi tiết)":
    st.markdown('<div class="main-header">Danh mục PCA Systems & Hình ảnh thiết bị</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Chọn hệ thống bên dưới để xem hình ảnh thực tế và thông tin chi tiết</div>', unsafe_allow_html=True)
    
    system_choice = st.selectbox(
        "🔍 Chọn hệ thống PCA System cần xem:",
        [
            "1. PRVX4 System",
            "2. PB6800 System",
            "3. VX#3, VX#2 System",
            "4. KT5000, KT6000, M5050, KT4000 System",
            "5. ADCMT 5450 System"
        ]
    )
    
    st.markdown("---")
    
    col_img, col_info = st.columns([1, 1])
    
    with col_img:
        st.subheader("📷 Hình ảnh / Sơ đồ kỹ thuật")
        if "PRVX4" in system_choice:
            if os.path.exists("prvx4.png"):
                st.image("prvx4.png", caption="PRVX4 System", use_container_width=True)
            else:
                st.info("🖼️ Đang hiển thị sơ đồ minh họa: **PRVX4 System**")
                st.warning("⚠️ Chưa tìm thấy file ảnh 'prvx4.png' trong thư mục. Vui lòng đặt file ảnh 'prvx4.png' cùng thư mục với app.")
                st.code("PRVX4 System Blueprint & Structure Layout", language="text")
        elif "PB6800" in system_choice:
            if os.path.exists("pb6800.png"):
                st.image("pb6800.png", caption="PB6800 System", use_container_width=True)
            else:
                st.info("🖼️ Đang hiển thị sơ đồ minh họa: **PB6800 System**")
                st.code("PB6800 System Mechanical Layout", language="text")
        elif "VX#3, VX#2 System" in system_choice:
            if os.path.exists("VX#3.png"):
                st.image("VX#3.png", caption="VX#3 System", use_container_width=True)
            else:
                st.info("🖼️ Đang hiển thị sơ đồ minh họa: **VX#3, VX#2 System**")
                st.code("VX Series Architecture Layout", language="text")
        elif "KT5000" in system_choice:
            st.info("🖼️ Đang hiển thị sơ đồ minh họa: **KT / M Series System**")
            st.code("KT5000 / KT6000 / M5050 / KT4000 Layout", language="text")
        elif "ADCMT" in system_choice:
            if os.path.exists("ADCMT.png"):
                st.image("ADCMT.png", caption="ADCMT 5450 System", use_container_width=True)
            else:
                st.info("🖼️ Đang hiển thị sơ đồ minh họa: **ADCMT 5450 System**")
                st.code("ADCMT 5450 Integration Scheme", language="text")
            
    with col_info:
        st.subheader("📋 Thông tin chi tiết & Thông số")
        if "PRVX4" in system_choice:
           with st.expander("🔬 PRVX4 System — Tổng quan thiết bị", expanded=True):
            st.markdown("""
    **PrecisionWoRx VX4 (PRVX4)** là hệ thống kiểm tra Probe Card độ chính xác cao,
    hỗ trợ các probe tip nhỏ và pitch nhỏ, với khả năng kiểm tra tự động và xử lý hình ảnh độ phân giải cao.
    """)
            st.markdown("### ⚡ Các phép đo chính")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("⚡ **Leakage** \n📐 **Planarity**")
            with col2:
                st.markdown("🎯 **Alignment** \n🔌 **Contact Resistance**")
            with col3:
                st.markdown("💪 **Probe Force** \n🔗 **Wire Checker**")
            
            st.markdown("### 📏 Thông số & khả năng hỗ trợ")
            st.markdown("""
    | 🔧 Hạng mục | 📋 Thông số |
    |:---|:---|
    | 🔹 **Probe Tip Diameter** | **5 – 250 µm** |
    | 💪 **Z-Axis Force** | **≤ 200 kg** |
    | 🔢 **Probe Count** | **> 100,000 probes** |
    | 🎯 **Direct Dock** | ✅ Hỗ trợ |
    | 🔌 **Switching** | Relay / Solid-State |
    | 🟦 **Membrane Probe Card** | ✅ Hỗ trợ |
    """)
            st.markdown("""
    **🛡️ Tính năng nổi bật:** Advanced ESD Management, Automatic Probe Inspection,
    hỗ trợ nhiều loại Check Plate và các công nghệ Probe Card phức tạp.

    **🏭 Thị trường:** CMOS Technology · Industrial
    """)
        elif "PB6800" in system_choice:
            with st.expander("🔬 PB6800 — Tổng quan thiết bị", expanded=True):
                st.markdown("""
    **PB6800** là hệ thống phân tích và kiểm tra Probe Card của
    **Probilt / Integrated Technology Corporation (ITC)**, được thiết kế
    cho nhà sản xuất và trung tâm sửa chữa Probe Card.

    Thiết bị hỗ trợ đo nhanh, chính xác và có độ lặp lại cao đối với nhiều
    loại Probe Card.
    """)
                st.markdown("### ⚡ Các phép đo chính")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(
            "⚡ **Leakage** \n"
            "🎯 **Alignment** \n"
            "📐 **Planarity** \n"
            "🔌 **Contact Resistance**"
        )
                with col2:
                    st.markdown(
            "💪 **Gram Force** \n"
            "🔍 **Tip Diameter** \n"
            "📏 **Tip Depth** \n"
            "🧹 **Scrub Analysis**"
        )
                with col3:
                    st.markdown(
            "🔗 **Wire Check** \n"
            "⚡ **OD Leakage** \n"
            "🔋 **Capacitor Leakage** \n"
            "🔧 **Relay / Resistor Test**"
        )
                st.markdown("### 📏 Thông số chính")
                st.markdown("""
    | 🔧 Hạng mục | 📋 Thông số |
    |:---|:---|
    | 🟢 **Chuck** | **12 inch** |
    | 📐 **Probe Array** | **≤ 300 mm** |
    | 🔌 **Channels** | **≤ 12,000 channels** |
    | 🎯 **Encoder Resolution** | **0.1 µm** |
    | ↔️ **XY Travel** | **12" × 8"** |
    | 💪 **Z-Axis Force** | **300 kg** |
    | ↕️ **Z Travel** | **0.75 inch** |
    | ⚡ **PMU** | **16-bit Precision Measurement Unit** |
    | 💻 **OS** | **Windows 10** |
    | 🖥️ **CPU** | **Intel Core i7** |
    """)
                st.markdown("""
    **🧪 Kiểm tra linh kiện tích hợp:** Relay · Capacitor · Resistor

    **🎯 Ứng dụng chính:** Probe Card Manufacturing · Probe Card Repair ·
    Electrical & Mechanical Characterization
    """)
        elif "VX#3" in system_choice:
            with st.expander("🔬 PRVX3 System — Tổng quan thiết bị", expanded=True):
                st.markdown("""
        **PRVX3** là thế hệ trước của **PRVX4**, thuộc dòng PrecisionWoRx,
        được sử dụng để kiểm tra và phân tích Probe Card trong sản xuất
        bán dẫn và sau quá trình repair.

        Hệ thống tập trung đánh giá **tình trạng cơ khí và điện** của Probe Card,
        đồng thời sử dụng hệ thống quang học và xử lý ảnh để giảm ảnh hưởng
        của người vận hành.
        """)
                st.markdown("### ⚡ Các phép đo chính")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(
                "🎯 **Alignment** \n"
                "📐 **Planarity** \n"
                "🔌 **Contact Resistance**"
            )
                with col2:
                    st.markdown(
                "⚡ **Leakage** \n"
                "💪 **Probe Force** \n"
                "🔗 **Wire Check**"
            )
                with col3:
                    st.markdown(
                "📍 **Needle Position** \n"
                "🔍 **Probe Inspection** \n"
                "🔢 **High Pin Count**"
            )
                st.markdown("### 🛠️ Chức năng kiểm tra")
                st.markdown("""
        | 🔧 Chức năng | 📋 Nội dung |
        |:---|:---|
        | 🎯 **Alignment** | Đo tọa độ X-Y, so sánh Golden Data, phát hiện kim lệch/cong/dịch chuyển |
        | 📐 **Planarity** | Đo độ cao Z, xác định probe cao/thấp bất thường |
        | 🔌 **Contact Resistance** | Kiểm tra điện trở tiếp xúc, phát hiện probe bẩn/oxy hóa/hư hỏng |
        | ⚡ **Leakage Test** | Kiểm tra rò điện giữa các kênh, phát hiện short/contamination |
        | 💪 **Probe Force** | Đo lực tác động của probe, đặc biệt quan trọng với Vertical Probe Card |
        """)
                st.markdown("### 📷 Hệ thống quang học")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("📷 **High-Resolution Camera**")
                with col2:
                    st.markdown("🔬 **Electronic Zoom Microscope**")
                with col3:
                    st.markdown("🤖 **Image Processing**")
                st.markdown("""
        Hệ thống hỗ trợ nhận dạng probe, tự động đo **tọa độ và hình dạng đầu kim**,
        giúp tăng độ chính xác và giảm ảnh hưởng của người vận hành.
        """)
                st.markdown("### 🧩 Probe Card hỗ trợ")
                st.markdown("""
        - 🟦 **Vertical Probe Card**
        - 🟨 **Cantilever Probe Card**
        - 🟩 **Membrane Probe Card**
        - 🔌 **Probe Card có Relay**
        - 🔢 **High Pin Count Probe Card**
        """)
        elif "KT5000" in system_choice:
            st.write("- **Tên thiết bị:** KT5000, KT6000, M5050, KT4000 System")
            st.write("- **Ứng dụng:** Nhóm hệ thống gia công và kiểm tra kỹ thuật đồng bộ.")
            st.write("- **Đặc điểm kỹ thuật:** Độ chính xác cấp độ micromet, độ bền vượt trội trong môi trường nhà máy.")
        elif "ADCMT" in system_choice:
            st.write("- **Tên thiết bị:** ADCMT 5450 System (Ultra High Resistance Meter) là thiết bị đo điện trở siêu cao và dòng rò siêu nhỏ của hãng ADCMT (ADC Corporation - Japan). Thiết bị thường được dùng trong đánh giá vật liệu cách điện, PCB/PCA, tụ điện, bán dẫn, pin lithium và các thử nghiệm dòng rò.")
            st.markdown("""
### 🔬 Ứng dụng

- ⚡ **Leakage Current** — Kiểm tra dòng rò giữa các net.
- 📐 **Insulation Resistance** — Đo điện trở cách điện sau khi vệ sinh PCB.
- 🧪 **Flux Residue** — Đánh giá ảnh hưởng của flux residue.
- 🔌 **Relay / Connector** — Kiểm tra độ cách điện.
- 🟩 **PCB Layer-to-Layer** — Đo điện trở cách điện giữa các lớp PCB.
- 🔋 **Capacitor Test** — Thử nghiệm tụ điện: Electrolytic, MLCC, Film.
- 🛠️ **Fixture / Test Jig** — Đánh giá vật liệu cách điện.

### 📊 So sánh với Megger thông thường

|  Thiết bị |  Giới hạn đo |
|:---|---:|
| 🔹 Megger | **TΩ (10¹² Ω)** |
| 🔬 ADCMT 5450 | **3 × 10¹⁷ Ω** |
| ⚡ Dòng đo nhỏ nhất | **1 fA** |
""")

# 3. CANTILEVER
elif menu == "Cantilever":
    if sub_menu == "1. Thiết bị & Hình ảnh":
        st.markdown('<div class="main-header">Cantilever: Thiết bị & Hình ảnh</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.info("🖼️ Hình ảnh thực tế kệ giá đỡ tay đòn Cantilever")
            st.code("Cantilever Racking System - Single/Double Sided", language="text")
        with col2:
            st.write("- **Ứng dụng:** Lưu trữ ống thép, thanh nhôm, vật liệu dài.")
            st.write("- **Tải trọng:** 500kg - 2500kg mỗi tay đòn.")
    # Gọi hàm quản lý Thư viện tài liệu với tên định danh là "Cant_Tools"
        render_doc_library("Cant_Tools")

    elif sub_menu == "2. Flowchart (Quy trình)":
        st.markdown('<div class="main-header">Cantilever: Flowchart (Quy trình lắp đặt)</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["1. Full Radius", "2. Lắp đặt khung chính", "3. Kiểm tra & Bàn giao"])
        with tab1:
            st.subheader("Quy trình Cho Card Yêu Cầu Làm Full Radius")
            if os.path.exists("FC_Full Radius.png"):
                st.image("FC_Full Radius.png", caption="Flow Chart Full Radius", width=1200)
            else:
                st.warning("⚠️ Chưa tìm thấy file ảnh 'FC_Full Radius.png'.")
        with tab2:
            st.subheader("Quy trình lắp đặt khung cấu kiện")
            st.code("Dựng cột trụ -> Siết bu-lông chân đế -> Lắp thanh giằng ngang -> Cố định tay đòn", language="text")
        with tab3:
            st.subheader("Quy trình nghiệm thu và bàn giao")
            st.code("Test tải trọng -> Vệ sinh khu vực -> Lập biên bản nghiệm thu -> Bàn giao sử dụng", language="text")

    elif sub_menu == "3. WI (Work Instruction)":
        st.markdown('<div class="main-header">Cantilever: Work Instruction (WI)</div>', unsafe_allow_html=True)
        st.write("1. **WI-CAN-01:** Hướng dẫn căn chỉnh độ nghiêng tay đòn.")
        st.write("2. **WI-CAN-02:** Quy trình cố định bu-lông chân cột xuống nền bê tông.")

    elif sub_menu == "4. DOC (Tài liệu)":
        # Gọi hàm quản lý Thư viện tài liệu với tên định danh là "Cantilever"
        render_doc_library("Cantilever")

    elif sub_menu == "5. Special Note (Lưu ý đặc biệt)":
        st.markdown('<div class="main-header">Cantilever: Special Note & Bảng theo dõi chỉnh sửa</div>', unsafe_allow_html=True)
        
        csv_file = "cantilever_table.csv"
        default_data = [
            ["Site A", "Intel", "Không tập trung tải trọng nặng ở đầu mút tay đòn.", "2026-01-15"],
            ["Site B", "Samsung", "Tay đòn thiết kế độ dốc hướng lên 2°-3° chống trượt hàng.", "2026-02-10"]
        ]
        
        df_notes = load_table_data(csv_file, default_data)
        
        # Ô tìm kiếm từ khóa
        search_query = st.text_input("🔍 Tìm kiếm thông tin trong bảng (Site, Khách hàng, Nội dung...):", key="search_can")
        
        st.markdown("### 📋 Bảng tổng hợp (Có thể chỉnh sửa trực tiếp các ô bên dưới):")
        # Cho phép chỉnh sửa trực tiếp trên bảng
        edited_df = st.data_editor(df_notes, num_rows="dynamic", use_container_width=True, key="editor_can")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("💾 Lưu thay đổi bảng", key="save_can_btn"):
                save_table_data(csv_file, edited_df)
                st.success("✅ Đã lưu các thay đổi trực tiếp vào file CSV thành công!")
                st.rerun()
                
        # Hiển thị kết quả tìm kiếm với màu Xanh lá cây dạ quang nổi bật
        if search_query.strip():
            st.markdown("---")
            st.markdown("### 🟢 Kết quả tìm kiếm (Được làm nổi bật):")
            mask = edited_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            filtered_df = edited_df[mask]
            
            if not filtered_df.empty:
                for idx, row in filtered_df.iterrows():
                    st.markdown(
                        f"""<div class="neon-highlight">
                        📍 <b>Site:</b> {row['Tester Site']} | 🏢 <b>Customer:</b> {row['Customer']}<br>
                        💬 <b>Note:</b> {row['Special Note']}<br>
                        📅 <b>Ngày:</b> {row['Ngày Cập Nhật']}
                        </div>""", 
                        unsafe_allow_html=True
                    )
            else:
                st.info("🔍 Không tìm thấy kết quả phù hợp với từ khóa của bạn.")

        st.markdown("---")
        st.subheader("➕ Thêm thông tin mới vào bảng")
        with st.form("add_cantilever_table_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_site = st.text_input("Tester Site:")
                new_customer = st.text_input("Customer:")
            with col2:
                new_date = st.date_input("Ngày Cập Nhật:", value=datetime.today())
                
            new_note = st.text_area("Special Note (Nội dung lưu ý):")
            submitted = st.form_submit_button("Thêm dòng mới vào Bảng & CSV")
            
            if submitted:
                if new_site.strip() and new_customer.strip() and new_note.strip():
                    new_row = pd.DataFrame([{
                        "Tester Site": new_site.strip(),
                        "Customer": new_customer.strip(),
                        "Special Note": new_note.strip(),
                        "Ngày Cập Nhật": str(new_date)
                    }])
                    updated_df = pd.concat([edited_df, new_row], ignore_index=True)
                    save_table_data(csv_file, updated_df)
                    st.success("✅ Đã thêm dòng mới thành công!")
                    st.rerun()
                else:
                    st.warning("⚠️ Vui lòng điền đầy đủ thông tin các trường bắt buộc!")

# 4. VERTICAL
elif menu == "Vertical":
    if sub_menu == "1. Thiết bị & Hình ảnh":
        st.markdown('<div class="main-header">Vertical: Thiết bị & Hình ảnh</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.info("🖼️ Sơ đồ hệ thống kệ Vertical Racking")
            st.code("Vertical Storage Racking - Direct Visual Identification", language="text")
        with col2:
            st.write("- **Ứng dụng:** Lưu trữ thanh đứng tối ưu diện tích.")
            st.write("- **Quy cách:** Chiều cao khung từ 2500mm đến 3500mm.")

    elif sub_menu == "2. Flowchart (Quy trình)":
        st.markdown('<div class="main-header">Vertical: Flowchart (Quy trình lắp đặt)</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["1. PB System", "2. Quy trình cho card WST", "3. Kiểm tra & Bàn giao"])
        with tab1:
            st.subheader("Quy trình Cho PB System")
            if os.path.exists("FC_PB System.png"):
                st.image("FC_PB System.png", caption="Flow Chart PB System", width=1200)
            else:
                st.warning("⚠️ Chưa tìm thấy file ảnh 'FC_PB System.png'.")
        with tab2:
            st.subheader("Quy trình cho card WST")
            st.markdown ("Apply từ today 8-Oct-26")
            st.markdown ("""Apply : Cho tất cả dạng card WST
               + Có Adjustable PIN và không có Adjustable PIN
               + Có MBA và no MBA""")
            
            if os.path.exists("FC_Card WST.png"):
                st.image("FC_Card WST.png", caption="Flow Chart card MST", width=1200)
            else:
                st.warning("⚠️ Chưa tìm thấy file ảnh 'FC_Card WST.png'.")
        with tab3:
            st.subheader("Quy trình nghiệm thu và bàn giao")
            st.code("Test tải trọng -> Vệ sinh khu vực -> Lập biên bản nghiệm thu -> Bàn giao sử dụng", language="text")

    elif sub_menu == "3. WI (Work Instruction)":
        st.markdown('<div class="main-header">Vertical: Work Instruction (WI)</div>', unsafe_allow_html=True)
        st.write("1. **WI-VER-01:** Hướng dẫn lắp ráp khung đỡ đứng.")
        st.write("2. **WI-VER-02:** Quy trình bố trí các thanh ngăn cách hàng.")

    elif sub_menu == "4. DOC (Tài liệu)":
        # Gọi hàm quản lý Thư viện tài liệu với tên định danh là "Cantilever"
        render_doc_library("Vertical")

    elif sub_menu == "5. Special Note (Lưu ý đặc biệt)":
        st.markdown('<div class="main-header">Vertical: Special Note & Bảng theo dõi chỉnh sửa</div>', unsafe_allow_html=True)
        
        csv_file = "vertical_table.csv"
        default_data = [
            ["Site 1", "Amkor", "Sắp xếp hàng hóa đối xứng và cân đối ở hai bên vách ngăn.", "2026-01-20"],
            ["Site 2", "ASE", "Sử dụng lớp đệm lót cao su chống trầy xước đế đỡ.", "2026-02-15"]
        ]
        
        df_notes = load_table_data(csv_file, default_data)
        
        search_query = st.text_input("🔍 Tìm kiếm thông tin trong bảng (Site, Khách hàng, Nội dung...):", key="search_ver")
        
        st.markdown("### 📋 Bảng tổng hợp (Có thể chỉnh sửa trực tiếp các ô bên dưới):")
        edited_df = st.data_editor(df_notes, num_rows="dynamic", use_container_width=True, key="editor_ver")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("💾 Lưu thay đổi bảng", key="save_ver_btn"):
                save_table_data(csv_file, edited_df)
                st.success("✅ Đã lưu các thay đổi trực tiếp vào file CSV thành công!")
                st.rerun()
                
        if search_query.strip():
            st.markdown("---")
            st.markdown("### 🟢 Kết quả tìm kiếm (Được làm nổi bật):")
            mask = edited_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            filtered_df = edited_df[mask]
            
            if not filtered_df.empty:
                for idx, row in filtered_df.iterrows():
                    st.markdown(
                        f"""<div class="neon-highlight">
                        📍 <b>Site:</b> {row['Tester Site']} | 🏢 <b>Customer:</b> {row['Customer']}<br>
                        💬 <b>Note:</b> {row['Special Note']}<br>
                        📅 <b>Ngày:</b> {row['Ngày Cập Nhật']}
                        </div>""", 
                        unsafe_allow_html=True
                    )
            else:
                st.info("🔍 Không tìm thấy kết quả phù hợp với từ khóa của bạn.")

        st.markdown("---")
        st.subheader("➕ Thêm thông tin mới vào bảng")
        with st.form("add_vertical_table_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_site = st.text_input("Tester Site:")
                new_customer = st.text_input("Customer:")
            with col2:
                new_date = st.date_input("Ngày Cập Nhật:", value=datetime.today())
                
            new_note = st.text_area("Special Note (Nội dung lưu ý):")
            submitted = st.form_submit_button("Thêm dòng mới vào Bảng & CSV")
            
            if submitted:
                if new_site.strip() and new_customer.strip() and new_note.strip():
                    new_row = pd.DataFrame([{
                        "Tester Site": new_site.strip(),
                        "Customer": new_customer.strip(),
                        "Special Note": new_note.strip(),
                        "Ngày Cập Nhật": str(new_date)
                    }])
                    updated_df = pd.concat([edited_df, new_row], ignore_index=True)
                    save_table_data(csv_file, updated_df)
                    st.success("✅ Đã thêm dòng mới thành công!")
                    st.rerun()
                else:
                    st.warning("⚠️ Vui lòng điền đầy đủ thông tin các trường bắt buộc!")

# 5. HOKKO
elif menu == "Hokko":
    if sub_menu == "1. Thiết bị & Hình ảnh":
        st.markdown('<div class="main-header">Hokko: MBA and Cable</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["1. MB001-2.5inch", "2. MB53-10inch", "3. Kiểm tra & Bàn giao"])
        with tab1:
            st.subheader("MB001-2.5inch")
            if os.path.exists("MB001-2.5inch.png"):
                st.image("MB001-2.5inch.png", caption="MB001-2.5inch", width=1200)
            else:
                st.warning("⚠️ Chưa tìm thấy file ảnh 'MB001-2.5inch.png'.")
        with tab2:
            st.subheader("MB53-10inch")
            st.image("MB53-10inch.png", caption="MB53-10inch", width=1200)
        with tab3:
            st.subheader("Quy trình nghiệm thu và bàn giao")
            st.code("Test tải trọng -> Vệ sinh khu vực -> Lập biên bản nghiệm thu -> Bàn giao sử dụng", language="text")
    elif sub_menu == "2. Flowchart (Quy trình)":
        st.markdown('<div class="main-header">Hokko: Flowchart (Quy trình thao tác)</div>', unsafe_allow_html=True)
        st.code("Start -> Kiểm tra linh kiện -> Lắp khớp nối định vị -> Siết chặt khớp khóa -> Kiểm tra độ chắc chắn", language="text")

    elif sub_menu == "3. WI (Work Instruction)":
        st.markdown('<div class="main-header">Hokko: Work Instruction (WI)</div>', unsafe_allow_html=True)
        st.write("1. **WI-HK-01:** Hướng dẫn lắp ráp linh kiện nhanh.")
        st.write("2. **WI-HK-02:** Quy trình bảo dưỡng các khớp nối định hình.")

    elif sub_menu == "4. DOC (Tài liệu)":
         # Gọi hàm quản lý Thư viện tài liệu với tên định danh là "Hokko"
        render_doc_library("Hokko")

    elif sub_menu == "5. Special Note (Lưu ý đặc biệt)":
        st.markdown('<div class="main-header">Hokko: Special Note & Bảng theo dõi chỉnh sửa</div>', unsafe_allow_html=True)
        
        csv_file = "hokko_table.csv"
        default_data = [
            ["Site Alpha", "TSMC", "Sử dụng đúng dụng cụ chuyên dụng khi tháo lắp khớp nối.", "2026-01-05"],
            ["Site Beta", "Sony", "Tuân thủ lực siết momen chuẩn cho khớp khóa.", "2026-02-20"]
        ]
        
        df_notes = load_table_data(csv_file, default_data)
        
        search_query = st.text_input("🔍 Tìm kiếm thông tin trong bảng (Site, Khách hàng, Nội dung...):", key="search_hok")
        
        st.markdown("### 📋 Bảng tổng hợp (Có thể chỉnh sửa trực tiếp các ô bên dưới):")
        edited_df = st.data_editor(df_notes, num_rows="dynamic", use_container_width=True, key="editor_hok")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("💾 Lưu thay đổi bảng", key="save_hok_btn"):
                save_table_data(csv_file, edited_df)
                st.success("✅ Đã lưu các thay đổi trực tiếp vào file CSV thành công!")
                st.rerun()
                
        if search_query.strip():
            st.markdown("---")
            st.markdown("### 🟢 Kết quả tìm kiếm (Được làm nổi bật):")
            mask = edited_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            filtered_df = edited_df[mask]
            
            if not filtered_df.empty:
                for idx, row in filtered_df.iterrows():
                    st.markdown(
                        f"""<div class="neon-highlight">
                        📍 <b>Site:</b> {row['Tester Site']} | 🏢 <b>Customer:</b> {row['Customer']}<br>
                        💬 <b>Note:</b> {row['Special Note']}<br>
                        📅 <b>Ngày:</b> {row['Ngày Cập Nhật']}
                        </div>""", 
                        unsafe_allow_html=True
                    )
            else:
                st.info("🔍 Không tìm thấy kết quả phù hợp với từ khóa của bạn.")

        st.markdown("---")
        st.subheader("➕ Thêm thông tin mới vào bảng")
        with st.form("add_hokko_table_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_site = st.text_input("Tester Site:")
                new_customer = st.text_input("Customer:")
            with col2:
                new_date = st.date_input("Ngày Cập Nhật:", value=datetime.today())
                
            new_note = st.text_area("Special Note (Nội dung lưu ý):")
            submitted = st.form_submit_button("Thêm dòng mới vào Bảng & CSV")
            
            if submitted:
                if new_site.strip() and new_customer.strip() and new_note.strip():
                    new_row = pd.DataFrame([{
                        "Tester Site": new_site.strip(),
                        "Customer": new_customer.strip(),
                        "Special Note": new_note.strip(),
                        "Ngày Cập Nhật": str(new_date)
                    }])
                    updated_df = pd.concat([edited_df, new_row], ignore_index=True)
                    save_table_data(csv_file, updated_df)
                    st.success("✅ Đã thêm dòng mới thành công!")
                    st.rerun()
                else:
                    st.warning("⚠️ Vui lòng điền đầy đủ thông tin các trường bắt buộc!")

# 6. PCA PRODUCTIVITY (Biểu đồ cột hiển thị theo từng Name/Nhân viên)
elif menu == "PCA Productivity":
    import plotly.express as px
    
    productivity_type = "Cant" if sub_menu == "PCA Cant Productivity" else "Vert"
    csv_prod_file = f"pca_{productivity_type.lower()}_productivity.csv"
    
    st.markdown(f'<div class="main-header">PCA Productivity: {sub_menu}</div>', unsafe_allow_html=True)
    
    default_prod_data = {
        "No": [1, 2, 3],
        "Employee Code": ["1505004", "1604006", "1810001"],
        "Name": ["Phan Đình Hùng", "Dương Tấn Đạt", "Ngô Quốc Khánh"],
        "Code": ["Dhung", "Tdat", "Qkhanh"],
        "Section": ["PCA", "PCA", "PCA"],
        "Productivity (PCA Standard Card/Month)": [291, 201, 174],
        "Productivity (PCA Standard Card/shift)": [8, 8, 7],
        "Employee Utilization": [0.964, 0.983, 0.927],
        "Mistake QTY": [0, 0, 0],
        "Mistake Ratio": [0.008, 0.0, 0.0],
        "Month": ["2026-08", "2026-08", "2026-08"]
    }
    
    df_prod = load_table_data(csv_prod_file, default_prod_data)
    
    # Bộ lọc theo tháng
    st.markdown("### 📅 Bộ lọc dữ liệu theo tháng")
    all_months = sorted(df_prod["Month"].astype(str).unique().tolist()) if "Month" in df_prod.columns else ["2026-08"]
    selected_months = st.multiselect("Chọn tháng xem dữ liệu (Bỏ trống để xem tất cả):", options=all_months, default=all_months)
    
    if selected_months:
        df_filtered = df_prod[df_prod["Month"].astype(str).isin(selected_months)].copy()
    else:
        df_filtered = df_prod.copy()
        
    st.markdown("### 📋 Bảng dữ liệu năng suất (Có thể chỉnh sửa trực tiếp hoặc thêm dòng mới):")
    
    edited_prod_df = st.data_editor(
        df_filtered, 
        num_rows="dynamic", 
        use_container_width=True, 
        key=f"editor_prod_{productivity_type}",
        column_config={
            "Employee Utilization": st.column_config.NumberColumn(
                "Employee Utilization",
                help="Tỷ lệ sử dụng nhân viên",
                format="%.1f%%"
            ),
            "Mistake Ratio": st.column_config.NumberColumn(
                "Mistake Ratio",
                help="Tỷ lệ lỗi",
                format="%.2f%%"
            )
        }
    )
    
    col_p1, _ = st.columns([1, 4])
    with col_p1:
        if st.button("💾 Lưu dữ liệu Năng suất", key=f"save_prod_{productivity_type}"):
            save_table_data(csv_prod_file, edited_prod_df)
            st.success("✅ Đã lưu dữ liệu năng suất vào CSV thành công!")
            st.rerun()
            
    st.markdown("---")
    st.markdown("### 📊 Biểu đồ thống kê theo từng nhân viên (Name)")
    
    if not edited_prod_df.empty:
        # Chuyển đổi các cột số liệu sang kiểu số học để vẽ biểu đồ chính xác
        chart_df = edited_prod_df.copy()
        chart_df["Productivity (PCA Standard Card/Month)"] = pd.to_numeric(chart_df["Productivity (PCA Standard Card/Month)"], errors="coerce")
        chart_df["Productivity (PCA Standard Card/shift)"] = pd.to_numeric(chart_df["Productivity (PCA Standard Card/shift)"], errors="coerce")
        chart_df["Employee Utilization"] = pd.to_numeric(chart_df["Employee Utilization"], errors="coerce")
        
        # 1. Biểu đồ cột: Productivity theo Month / Name
        fig1 = px.bar(
                chart_df, x="Name", y="Productivity (PCA Standard Card/Month)",
                color="Month" if len(all_months) > 1 else None,
                barmode="group",
                title="Productivity (PCA Standard Card/Month) theo Nhân viên",
                text_auto=True,
                template="plotly_dark"
            )
        fig1.update_layout(xaxis_title="Nhân viên (Name)", yaxis_title="Card/Month")
        st.plotly_chart(fig1, use_container_width=True)
            
            # 2. Biểu đồ cột: Productivity per shift theo Name
        fig2 = px.bar(
                chart_df, x="Name", y="Productivity (PCA Standard Card/shift)",
                color="Month" if len(all_months) > 1 else None,
                barmode="group",
                title="Productivity (PCA Standard Card/shift) theo Nhân viên",
                text_auto=True,
                template="plotly_dark"
            )
        fig2.update_layout(xaxis_title="Nhân viên (Name)", yaxis_title="Card/shift")
        st.plotly_chart(fig2, use_container_width=True)
            
            # 3. Biểu đồ cột: Employee Utilization theo Name (Dùng update_yaxes đúng chuẩn)
        fig3 = px.bar(
                chart_df, x="Name", y="Employee Utilization",
                color="Month" if len(all_months) > 1 else None,
                barmode="group",
                title="Employee Utilization theo Nhân viên",
                text_auto=True,
                template="plotly_dark"
            )
        fig3.update_layout(xaxis_title="Nhân viên (Name)", yaxis_title="Utilization")
        fig3.update_yaxes(tickformat=',.0%')
        st.plotly_chart(fig3, use_container_width=True)
        
    else:
        st.info("ℹ Chưa có dữ liệu để hiển thị biểu đồ.")

# 7. TÀI LIỆU & TRA CỨU
elif menu == "Tài liệu & Tra cứu":
    st.markdown('<div class="main-header">Tra cứu tài liệu & Biểu mẫu</div>', unsafe_allow_html=True)
    st.write("Tải về các biểu mẫu bàn giao, biên bản nghiệm thu và bản vẽ kỹ thuật tham khảo.")
    st.download_button(
        label="📥 Tải xuống Biên bản nghiệm thu mẫu (PDF)",
        data=b"Sample PDF Content for Handover Protocol",
        file_name="Bien_ban_nghiem_thu_PCA.pdf",
        mime="application/pdf"
    )
    st.download_button(
        label="📥 Tải xuống Catalogue tổng hợp 2026 (PDF)",
        data=b"Sample Catalogue Content",
        file_name="Catalogue_PCA_2026.pdf",
        mime="application/pdf"
    )
    # Gọi hàm quản lý Thư viện tài liệu với tên định danh là "Tài liệu"
    render_doc_library("Tài Liệu")
