import streamlit as st
import pandas as pd
import requests

API_BASE_URL = "https://wpc.notdot.link"

# 获取账号信息
def get_accounts():
    response = requests.get(f"{API_BASE_URL}/accounts")
    return response.json()

# 启动爬虫
def start_spider(account):
    response = requests.post(f"{API_BASE_URL}/start", json={"account": account})
    return response.json()

# 停止爬虫
def stop_spider(account):
    response = requests.post(f"{API_BASE_URL}/stop", json={"account": account})
    return response.json()

# 添加账号
def add_account(account, account_type, password):
    response = requests.post(f"{API_BASE_URL}/add", json={
        "account": account,
        "type": account_type,
        "password": password
    })
    return response.json()

# 删除账号
def delete_account(account):
    response = requests.post(f"{API_BASE_URL}/delete", json={"account": account})
    return response.json()

# 获取日志
def get_logs(account):
    response = requests.post(f"{API_BASE_URL}/log", json={"account": account})
    return response.json()

# Streamlit App
st.set_page_config(layout="wide")
st.title("爬虫任务管理")

# 侧边栏
st.sidebar.title("导航")
pages = ["账号管理"] + [acc['account'] for acc in get_accounts()]
choice = st.sidebar.radio("选择页面", pages)

if choice == "账号管理":
    # 账号管理页面
    st.header("账号管理")

    # 创建两列布局
    col1, col2 = st.columns([2, 1])

    with col1:
        # 添加账号
        with st.form("account_form"):
            st.subheader("添加账号")
            account = st.text_input("账号")
            account_type = st.selectbox("类型", ["干部", "华医", "普法", "公需课"])
            password = st.text_input("密码", type="password")
            col_submit, col_import = st.columns(2)
            with col_submit:
                submitted = st.form_submit_button("添加")
            with col_import:
                import_button = st.form_submit_button("导入Excel")
            
            if submitted:
                result = add_account(account, account_type, password)
                if result.get('status') == 'success':
                    st.success(f"账号 {account} 添加成功")
                else:
                    st.error(f"添加失败: {result.get('message', '未知错误')}")
                st.rerun()
            
            if import_button:
                uploaded_file = st.file_uploader("选择Excel文件 (.xlsx)", type="xlsx")
                if uploaded_file:
                    data = pd.read_excel(uploaded_file)
                    success_count = 0
                    for _, row in data.iterrows():
                        result = add_account(row['账号'], row['类型'], row['密码'])
                        if result.get('status') == 'success':
                            success_count += 1
                    st.success(f"成功导入 {success_count} 个账号")
                    st.rerun()

    # 显示账号表格
    st.subheader("账号总览")
    accounts_data = get_accounts()
    accounts_df = pd.DataFrame(accounts_data)
    
    # 使用 st.dataframe() 并设置 use_container_width=True
    st.dataframe(accounts_df, use_container_width=True)

    # 可选：添加一些样式来突出显示表格
    st.markdown("""
    <style>
    .stDataFrame {
        border: 2px solid #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

else:
    # 单个账号页面
    st.header(f"账号: {choice}")

    # 操作按钮
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("启动"):
            result = start_spider(choice)
            if result.get('status') == 'success':
                st.success(f"{choice} 已启动")
            else:
                st.error(f"启动失败: {result.get('message', '未知错误')}")
    with col2:
        if st.button("停止"):
            result = stop_spider(choice)
            if result.get('status') == 'success':
                st.success(f"{choice} 已停止")
            else:
                st.error(f"停止失败: {result.get('message', '未知错误')}")
    with col3:
        if st.button("删除"):
            result = delete_account(choice)
            if result.get('status') == 'success':
                st.success(f"{choice} 已删除")
                st.rerun()
            else:
                st.error(f"删除失败: {result.get('message', '未知错误')}")

    # 显示日志
    st.subheader("日志")
    logs = get_logs(choice)
    if logs.get('status') == 'success':
        log_text = logs.get('logs', '')
        st.text_area("最近的日志", log_text, height=400)
    else:
        st.error(f"获取日志失败: {logs.get('message', '未知错误')}")

# 添加页脚
st.sidebar.markdown("---")
st.sidebar.info("© 2023 爬虫任务管理系统")
