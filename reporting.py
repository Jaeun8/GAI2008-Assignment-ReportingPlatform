import folium
import streamlit as st
from streamlit_folium import st_folium
from datetime import date
import random
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import smtplib
from email.mime.text import MIMEText

class Complaint:
    def __init__(self, location, author, complaint_type, content, report_date, receipt_number):
        self.location = location
        self.author = author
        self.complaint_type = complaint_type
        self.content = content
        self.report_date = report_date
        self.receipt_number = receipt_number

    def __str__(self):
        return f"""
위치: {self.location}
작성자: {self.author}
유형: {self.complaint_type}
내용: {self.content}
작성일: {self.report_date}
접수번호: {self.receipt_number}"""

def send_email_notification(complaint_instance):
    try:
        email_sender = st.secrets.get("email", {}).get("gmail", "")
        email_password = st.secrets.get("email", {}).get("password", "")
        admin_email = st.secrets.get("email", {}).get("admin_email", "")
        
        if not all([email_sender, email_password, admin_email]):
            return False, "이메일 설정이 완료되지 않았습니다. secrets.toml에 이메일 설정을 확인해주세요."
        
        subject = f"🚨 새로운 민원 접수 알림 - {complaint_instance.receipt_number}"
        
        body = f"""
새로운 민원이 접수되었습니다! 🚨

📋 민원 상세 정보:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 접수번호: {complaint_instance.receipt_number}
• 작성자: {complaint_instance.author}
• 민원 유형: {complaint_instance.complaint_type}
• 위치: {complaint_instance.location}
• 작성일: {complaint_instance.report_date}

📝 민원 내용:
{complaint_instance.content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 처리 안내:
새로운 민원이 접수되었습니다. 빠른 시일 내에 검토 및 처리 부탁드립니다.
구글 시트에서 상세 내용을 확인하실 수 있습니다.

---
이 이메일은 민원 접수 시스템에서 자동으로 발송되었습니다.
발송 시간: {complaint_instance.report_date}
        """
        
        msg = MIMEText(body)
        msg['From'] = email_sender
        msg['To'] = admin_email
        msg['Subject'] = subject
        
        # SMTP 서버 연결 및 이메일 전송
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, admin_email, msg.as_string())
        server.quit()
        
        return True, "이메일 알림이 성공적으로 전송되었습니다."
        
    except Exception as e:
        return False, f"이메일 전송 실패: {str(e)}"

def get_gsheet_connection():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        test_df = conn.read(worksheet="시트1", ttl=0)
        return conn, "시트1"
    except Exception as e1:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            test_df = conn.read(worksheet="Sheet1", ttl=0)
            return conn, "Sheet1"
        except Exception as e2:
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                test_df = conn.read(ttl=0)
                return conn, None
            except Exception as e3:
                st.error(f"구글 시트 연결 오류:\n- 시트1: {str(e1)}\n- Sheet1: {str(e2)}\n- 기본시트: {str(e3)}")
                return None, None

def save_to_gsheet(complaint_instance):
    conn, worksheet_name = get_gsheet_connection()

    if not conn:
        return False, "구글 시트 연결에 실패했습니다."
    
    try:
        columns = ["접수번호", "위치", "작성자", "유형", "내용", "작성일"]
        
        if worksheet_name:
            df = conn.read(worksheet=worksheet_name, usecols=list(range(len(columns))), ttl=0)
        else:
            df = conn.read(usecols=list(range(len(columns))), ttl=0)
        
        if df.empty or len(df.columns) == 0:
            df = pd.DataFrame(columns=columns)
        else:
            if len(df.columns) >= len(columns):
                df.columns = columns[:len(df.columns)]
            else:
                df = pd.DataFrame(columns=columns)
        
        new_row = {
            "접수번호": complaint_instance.receipt_number,
            "위치": complaint_instance.location,
            "작성자": complaint_instance.author,
            "유형": complaint_instance.complaint_type,
            "내용": complaint_instance.content,
            "작성일": complaint_instance.report_date
        }
        
        new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        if worksheet_name:
            conn.update(worksheet=worksheet_name, data=new_df)
        else:
            conn.update(data=new_df)
        
        return True, "성공적으로 저장되었습니다."

    except Exception as e:
        return False, f"저장 중 오류 발생: {str(e)}"

st.markdown("""
<style>
    .main .block-container {
        max-width: 100%;
        padding-top: 2.5rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        padding-bottom: 2.5rem;
    }
    /* 다크모드 지원 */
    @media (prefers-color-scheme: dark) {
        .stForm {
            background-color: #23272f !important;
            border: 1px solid #444950 !important;
        }
        .stSuccess {
            background-color: #1e5631 !important;
            color: #e6ffe6 !important;
        }
        .stInfo {
            background-color: #22304a !important;
            color: #cce0ff !important;
        }
    }
    @media (prefers-color-scheme: light) {
        .stForm {
            background-color: #f8f9fa !important;
            border: 1px solid #dee2e6 !important;
        }
        .stSuccess {
            background-color: #d1e7dd !important;
            color: #0f5132 !important;
        }
        .stInfo {
            background-color: #e7f1ff !important;
            color: #084298 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title('📝 민원 등록하기')

if "marker_location" not in st.session_state:
    st.session_state.marker_location = [37.564375, 126.938871]
    st.session_state.zoom = 16

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 위치 선택")
    
    m = folium.Map(
        location=st.session_state.marker_location, 
        zoom_start=st.session_state.zoom,
        tiles='OpenStreetMap'
    )

    popup_html = """
    <div style="font-family: Arial, sans-serif; white-space: nowrap; font-size: 14px;">
        <b>민원 위치<br>
    </div>
    """

    folium.Marker(
        location=st.session_state.marker_location,
        popup=folium.Popup(popup_html, max_width=200),
        tooltip="클릭하거나 드래그하여 위치를 변경하세요",
        draggable=True,
        icon=folium.Icon(color='red', icon='exclamation-sign')
    ).add_to(m)
    
    m.add_child(folium.LatLngPopup())

    map_data = st_folium(
        m, 
        width="100%", 
        height=655,
        key="folium_map",
        returned_objects=["last_object_clicked", "last_clicked", "last_object_dragged"]
    )

with col2:
    st.subheader("📝 민원 정보 입력")
    
    with st.expander("🔗 시스템 연결 상태", expanded=False):

        conn, worksheet_name = get_gsheet_connection()
        if conn:
            st.success(f"✅ 구글 시트 연결됨")
            if worksheet_name:
                st.info(f"📄 워크시트: {worksheet_name}")
        else:
            st.error("❌ 구글 시트 연결 실패")
        
        email_config = st.secrets.get("email", {})
        if email_config.get("gmail") and email_config.get("admin_email"):
            st.success("✅ 이메일 알림 설정됨")
            st.info(f"📧 관리자 이메일: {email_config.get('admin_email')}")
        else:
            st.warning("⚠️ 이메일 알림 설정 필요")
            st.markdown("""
            **이메일 설정 안내:**
            secrets.toml 파일에 다음 설정을 추가하세요:
            ```
            [email]
            gmail = "your-email@gmail.com"
            password = "your-app-password"
            admin_email = "admin@example.com"
            ```
            """)
    
    lat, lng = st.session_state.marker_location
    st.info(f"**선택된 위치**\n위도: {lat:.6f}\n경도: {lng:.6f}")
    
    with st.form("complaint_form"):
        name = st.text_input("민원 작성자 *", placeholder="이름을 입력하세요")
        
        complaint_type = st.selectbox(
            "민원 유형 *",
            ["도로/교통", "환경/위생", "안전", "시설물", "기타"]
        )
        
        content = st.text_area(
            "민원 내용 *", 
            placeholder="민원 내용을 자세히 입력하세요",
            height=150
        )
        
        report_date = st.date_input("작성 날짜", value=date.today())
        
        submit_button = st.form_submit_button("민원 신청하기", use_container_width=True)
        
        if submit_button:
            if name and content:
                receipt_number = f"CR{date.today().strftime('%Y%m%d')}{random.randint(1000, 9999)}"

                complaint_instance = Complaint(
                    location=f"{lat:.6f}, {lng:.6f}",
                    author=str(name).strip(),
                    complaint_type=str(complaint_type),
                    content=str(content).strip(),
                    report_date=str(report_date),
                    receipt_number=str(receipt_number)
                )

                save_success, save_message = save_to_gsheet(complaint_instance)

                email_success, email_message = send_email_notification(complaint_instance)
                
                if save_success:
                    st.success("✅ 민원이 정상적으로 접수되고 구글 시트에 저장되었습니다!")

                    if email_success:
                        st.success("📧 관리자에게 이메일 알림이 전송되었습니다!")
                    else:
                        st.warning(f"⚠️ 이메일 전송 실패: {email_message}")

                    st.markdown("### 📋 접수 정보")
                    st.text(str(complaint_instance))
                else:
                    st.error(f"❌ 저장 실패: {save_message}")
                    
                    st.warning("⚠️ 임시로 로컬에 저장된 민원 정보:")
                    st.text(str(complaint_instance))
                
            else:
                st.error("❌ 필수 항목을 모두 입력해주세요!")

if map_data:
    if map_data.get("last_object_dragged"):
        new_lat = map_data["last_object_dragged"]["lat"]
        new_lng = map_data["last_object_dragged"]["lng"]
        if [new_lat, new_lng] != st.session_state.marker_location:
            st.session_state.marker_location = [new_lat, new_lng]
            st.rerun()
    
    elif map_data.get("last_clicked"):
        new_lat = map_data["last_clicked"]["lat"]
        new_lng = map_data["last_clicked"]["lng"]
        if [new_lat, new_lng] != st.session_state.marker_location:
            st.session_state.marker_location = [new_lat, new_lng]
            st.rerun()

st.markdown("---")
st.markdown("""
### 📖 사용법 안내
1. **위치 선택**: 지도에서 원하는 위치를 클릭하거나 마커를 드래그하여 위치를 설정하세요
2. **정보 입력**: 우측 폼에서 민원 관련 정보를 입력하세요
3. **신청 완료**: '민원 신청하기' 버튼을 클릭하여 민원을 접수하세요
4. **자동 저장**: 접수된 민원은 자동으로 구글 시트에 저장됩니다
5. **이메일 알림**: 민원 접수 시 관리자에게 자동으로 이메일 알림이 전송됩니다

### 📧 이메일 설정 방법
이메일 알림 기능을 사용하려면 `secrets.toml` 파일에 다음과 같이 설정하세요:

```toml
[email]
gmail = "your-email@gmail.com"
password = "your-app-password"  # Gmail 앱 비밀번호
admin_email = "admin@example.com"
```

**Gmail 사용 시 주의사항:**
- 2단계 인증을 활성화하고 앱 비밀번호를 생성해야 합니다
- 일반 비밀번호가 아닌 앱 비밀번호를 사용해야 합니다
""")

st.markdown("""
<style>
    .stForm {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    
    .stSuccess {
        padding: 15px;
        border-radius: 5px;
    }
    
    .stInfo {
        padding: 10px;
        border-radius: 5px;
        font-size: 14px;
    }
                    
    .streamlit-expanderHeader {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)