import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="PCA Technical Handbook",
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
    /* Style cho kết quả tìm kiếm nổi bật màu xanh lá cây dạ quang */
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
# HÀM HỖ TRỢ QUẢN LÝ BẢNG DỮ LIỆU CSV CHO SPECIAL NOTE
# ---------------------------------------------------------
def load_table_data(filename, default_data):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            expected_cols = ["Tester Site", "Customer", "Special Note", "Ngày Cập Nhật"]
            if all(col in df.columns for col in expected_cols):
                return df
        except Exception:
            pass
    # Nếu chưa có file hoặc lỗi, tạo file mặc định
    df_default = pd.DataFrame(default_data, columns=["Tester Site", "Customer", "Special Note", "Ngày Cập Nhật"])
    df_default.to_csv(filename, index=False)
    return df_default

def save_table_data(filename, df):
    df.to_csv(filename, index=False)

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
        "Tài liệu & Tra cứu"
    ]
)

def render_sub_menu(category_name):
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"📁 **Thư mục con ({category_name}):**")
    sub_choice = st.sidebar.radio(
        "Chọn nội dung:",
        [
            "1. Thiết bị & Hình ảnh",
            "2. Flowchart (Quy trình)",
            "3. WI (Work Instruction)",
            "4. DOC (Tài liệu)",
            "5. Special Note (Lưu ý đặc biệt)"
        ],
        key=f"sub_{category_name}"
    )
    return sub_choice

sub_menu = None
if menu in ["Cantilever", "Vertical", "Hokko"]:
    sub_menu = render_sub_menu(menu)

st.sidebar.markdown("---")
st.sidebar.info("📌 **Phiên bản:** 1.6.0 \n📅 **Cập nhật:** 2026 \n🏢 **Phòng Kỹ thuật PCA**")

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

elif menu == "PCA Systems (Chi tiết)":
    st.markdown('<div class="main-header">Danh mục PCA Systems & Hình ảnh thiết bị</div>', unsafe_allow_html=True)
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
        st.info(f"🖼️ Đang hiển thị thông tin: **{system_choice}**")
    with col_info:
        st.subheader("📋 Thông tin chi tiết")
        st.write("Chọn hệ thống tương ứng để xem các thông số kỹ thuật chuẩn hóa.")

elif menu == "Kiến thức chung":
    st.markdown('<div class="main-header">Kiến thức chung & Tiêu chuẩn kỹ thuật</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["⚠️ Quy định an toàn", "🧱 Tiêu chuẩn vật liệu", "🛠️ Hướng dẫn lắp đặt"])
    with tab1:
        st.subheader("Quy định an toàn lao động khi thi công")
        st.write("1. Luôn đeo nón bảo hộ, giày bảo hộ và dây an toàn.")
    with tab2:
        st.subheader("Tiêu chuẩn vật liệu thép & bề mặt")
        st.write("- Sử dụng thép tiêu chuẩn SS400 / Q235B.")
    with tab3:
        st.subheader("Quy trình lắp đặt tổng quát")
        st.write("- Khảo sát mặt bằng và kiểm tra cao độ sàn bê tông.")

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
        st.markdown('<div class="main-header">Cantilever: Documentation (DOC)</div>', unsafe_allow_html=True)
        st.download_button("📥 Tải Catalogue & Bản vẽ Cantilever (PDF)", data=b"Cantilever PDF", file_name="Cantilever_Catalogue.pdf")

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
        st.code("Start -> Khảo sát vị trí -> Lắp khung đỡ đứng -> Chia ngăn phân cách -> Kiểm tra & Bàn giao", language="text")

    elif sub_menu == "3. WI (Work Instruction)":
        st.markdown('<div class="main-header">Vertical: Work Instruction (WI)</div>', unsafe_allow_html=True)
        st.write("1. **WI-VER-01:** Hướng dẫn lắp ráp khung đỡ đứng.")
        st.write("2. **WI-VER-02:** Quy trình bố trí các thanh ngăn cách hàng.")

    elif sub_menu == "4. DOC (Tài liệu)":
        st.markdown('<div class="main-header">Vertical: Documentation (DOC)</div>', unsafe_allow_html=True)
        st.download_button("📥 Tải tài liệu kỹ thuật Vertical (PDF)", data=b"Vertical PDF", file_name="Vertical_Documentation.pdf")

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
        st.markdown('<div class="main-header">Hokko: Thiết bị & Hình ảnh</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.info("🖼️ Hình ảnh linh kiện và phụ kiện kết cấu Hokko")
            st.code("Hokko Precision Mechanical & Fast Assembly Components", language="text")
        with col2:
            st.write("- **Ứng dụng:** Linh kiện lắp ráp nhanh, khớp nối chuyên dụng.")
            st.write("- **Đặc điểm:** Độ bền cao, kết cấu linh hoạt.")

    elif sub_menu == "2. Flowchart (Quy trình)":
        st.markdown('<div class="main-header">Hokko: Flowchart (Quy trình thao tác)</div>', unsafe_allow_html=True)
        st.code("Start -> Kiểm tra linh kiện -> Lắp khớp nối định vị -> Siết chặt khớp khóa -> Kiểm tra độ chắc chắn", language="text")

    elif sub_menu == "3. WI (Work Instruction)":
        st.markdown('<div class="main-header">Hokko: Work Instruction (WI)</div>', unsafe_allow_html=True)
        st.write("1. **WI-HK-01:** Hướng dẫn lắp ráp linh kiện nhanh.")
        st.write("2. **WI-HK-02:** Quy trình bảo dưỡng các khớp nối định hình.")

    elif sub_menu == "4. DOC (Tài liệu)":
        st.markdown('<div class="main-header">Hokko: Documentation (DOC)</div>', unsafe_allow_html=True)
        st.download_button("📥 Tải Catalogue Hokko 2026 (PDF)", data=b"Hokko PDF", file_name="Hokko_Catalogue_2026.pdf")

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

# 6. TÀI LIỆU & TRA CỨU
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
