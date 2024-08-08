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
