import streamlit as st
import pandas as pd
import requests
from time import sleep

API_BASE_URL = "http://wpc.notdot.link"

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
st.title("爬虫任务管理")

# 自动刷新间隔auto_refresh_interval = st.

# 添加账号
with st.form("account_form"):
    account = st.text_input("账号")
    account_type = st.text_input("类型")
    password = st.text_input("密码", type="password")
    submitted = st.form_submit_button("添加")
    if submitted:
        add_account(account, account_type, password)
        st.success(f"账号 {account} 添加成功")
        st.rerun()  # 重新运行以更新页面

# 获取并展示账号信息
accounts_data = get_accounts()
accounts_df = pd.DataFrame(accounts_data)

# 选择操作的账号
selected_accounts = st.multiselect("选择账号进行操作", accounts_df['account'])

# 操作按钮
if st.button("启动选中的账号"):
    for acc in selected_accounts:
        start_spider(acc)
    st.success("选中的账号已启动")
    st.rerun()  # 重新运行以更新页面

if st.button("停止选中的账号"):
    for acc in selected_accounts:
        stop_spider(acc)
    st.success("选中的账号已停止")
    st.rerun()  # 重新运行以更新页面

if st.button("删除选中的账号"):
    for acc in selected_accounts:
        delete_account(acc)
    st.success("选中的账号已删除")
    st.rerun()  # 重新运行以更新页面

# 导入Excel文件并添加账号
uploaded_file = st.file_uploader("导入账号 (.xlsx)", type="xlsx")
if uploaded_file:
    data = pd.read_excel(uploaded_file)
    for _, row in data.iterrows():
        add_account(row['账号'], row['类型'], row['密码'])
    st.success("Excel文件中的账号已导入")
    st.rerun()  # 重新运行以更新页面

# 显示账号表格
st.dataframe(accounts_df)

# 展示选中账号的日志
if selected_accounts:
    for acc in selected_accounts:
        if st.button(f"显示 {acc} 的日志"):
            logs = get_logs(acc)
            st.text_area(f"{acc} 的日志", "\n".join(logs['logs'][-50:]))
