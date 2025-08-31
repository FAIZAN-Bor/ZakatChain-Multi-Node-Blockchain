"""
Enhanced Streamlit Web Application for Multi-Node Zakat Blockchain Simulation
A user-friendly interface with professional color scheme and multi-node support
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from blockchain import ZakatBlockchain, Transaction
import time
from datetime import datetime


# Custom CSS for professional styling
def load_custom_css():
    """Load custom CSS for better styling"""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #1e3a8a;
        --secondary-color: #3b82f6;
        --accent-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --success-color: #22c55e;
        --background-color: #f8fafc;
        --card-background: #ffffff;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid var(--primary-color);
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    /* Status indicators */
    .status-valid {
        color: var(--success-color);
        font-weight: bold;
    }
    
    .status-invalid {
        color: var(--danger-color);
        font-weight: bold;
    }
    
    .status-warning {
        color: var(--warning-color);
        font-weight: bold;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Node cards */
    .node-card {
        background: var(--card-background);
        border: 2px solid var(--border-color);
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .node-card:hover {
        border-color: var(--secondary-color);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .node-active {
        border-color: var(--success-color);
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    }
    
    /* Info boxes */
    .info-box {
                # linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
        background: black ; 
        border: 1px solid var(--secondary-color);
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .zakat-info {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
        border: 1px solid var(--accent-color);
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = None
    if 'creator_roll_number' not in st.session_state:
        st.session_state.creator_roll_number = ""
    if 'current_user' not in st.session_state:
        st.session_state.current_user = ""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False


def display_header():
    """Display main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🕌 Zakat Blockchain Network</h1>
        <p>Multi-Node Islamic Finance Blockchain Simulation</p>
    </div>
    """, unsafe_allow_html=True)


def create_blockchain_interface():
    """Create the main blockchain interface"""
    load_custom_css()
    display_header()
    
    # Sidebar for blockchain management
    with st.sidebar:
        st.markdown("### 🚀 Blockchain Management")
        
        if not st.session_state.initialized:
            display_initialization_panel()
        else:
            display_node_management_panel()
    
    # Main content area
    if st.session_state.initialized and st.session_state.blockchain:
        display_main_dashboard()
    else:
        display_welcome_screen()


def display_initialization_panel():
    """Display blockchain initialization panel"""
    st.markdown("#### Initialize New Blockchain")
    
    creator_roll_number = st.text_input(
        "Creator Roll Number",
        placeholder="e.g., 2021-CS-001",
        help="This will be the blockchain creator and seed key"
    )
    
    initial_balance = st.number_input(
        "Initial Balance (coins)",
        min_value=100.0,
        max_value=1000.0,
        value=200.0,
        step=10.0,
        help="Starting balance for the creator node"
    )
    
    if st.button("🚀 Create Blockchain", type="primary"):
        if creator_roll_number:
            st.session_state.blockchain = ZakatBlockchain(creator_roll_number, initial_balance)
            st.session_state.creator_roll_number = creator_roll_number
            st.session_state.current_user = creator_roll_number
            st.session_state.initialized = True
            st.success(f"✅ Blockchain created for {creator_roll_number}!")
            st.rerun()
        else:
            st.error("❌ Please enter a valid roll number!")


def display_node_management_panel():
    """Display node management panel"""
    blockchain = st.session_state.blockchain
    
    st.markdown("#### 🌐 Network Status")
    stats = blockchain.get_blockchain_stats()
    
    # Use st.info instead of custom HTML for better compatibility
    st.info(f"""
    **Creator:** {st.session_state.creator_roll_number}
    
    **Total Nodes:** {stats['total_nodes']}
    
    **Active Nodes:** {stats['active_nodes']}
    
    **Chain Status:** {'✅ Valid' if stats['chain_valid'] else '❌ Invalid'}
    """)
    
    # Current user selection
    all_nodes = list(blockchain.get_all_nodes().keys())
    current_user = st.selectbox(
        "👤 Current User",
        all_nodes,
        index=all_nodes.index(st.session_state.current_user) if st.session_state.current_user in all_nodes else 0,
        help="Select which node you're operating as"
    )
    
    if current_user != st.session_state.current_user:
        st.session_state.current_user = current_user
        st.rerun()
    
    st.markdown("---")
    
    # Add new node
    st.markdown("#### ➕ Add New Node")
    new_roll_number = st.text_input(
        "New Node Roll Number",
        placeholder="e.g., 2021-CS-002",
        help="Roll number for the new node"
    )
    
    new_node_balance = st.number_input(
        "Initial Balance",
        min_value=50.0,
        max_value=500.0,
        value=200.0,
        step=10.0,
        help="Starting balance for the new node"
    )
    
    if st.button("➕ Add Node"):
        if new_roll_number:
            if blockchain.add_node(new_roll_number, new_node_balance):
                st.success(f"✅ Node {new_roll_number} added successfully!")
                st.rerun()
            else:
                st.error(f"❌ Node {new_roll_number} already exists!")
        else:
            st.error("❌ Please enter a valid roll number!")
    
    st.markdown("---")
    
    # Reset option
    if st.button("🔄 Reset Blockchain", help="Start fresh with a new blockchain"):
        st.session_state.blockchain = None
        st.session_state.initialized = False
        st.session_state.creator_roll_number = ""
        st.session_state.current_user = ""
        st.rerun()


def display_welcome_screen():
    """Display welcome screen when blockchain is not initialized"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🌟 Welcome to Multi-Node Zakat Blockchain!")
        
        st.success("### 🚀 Enhanced Features:")
        st.markdown("""
        - **🌐 Multi-Node Support:** Add multiple students/participants
        - **🔐 Secure Hashing:** Creator's roll number as unique seed
        - **💰 Automatic Zakat:** 2.5% Islamic obligation calculation
        - **📊 Real-time Analytics:** Interactive charts and statistics
        - **⛏️ Collaborative Mining:** All nodes can mine blocks
        - **🎨 Professional UI:** Modern design with proper color scheme
        """)
        
        st.info("### 🕌 About Zakat:")
        st.markdown("""
        Zakat is the third pillar of Islam, requiring Muslims to donate 2.5% of their wealth annually to help those in need. This blockchain simulation demonstrates how modern technology can facilitate transparent and immutable religious financial obligations.
        """)
        
        st.warning("### 🎯 Getting Started:")
        st.markdown("""
        1. Enter your roll number in the sidebar to create the blockchain
        2. Add other students as nodes to the network
        3. Switch between different user accounts
        4. Create transactions and mine blocks collaboratively
        5. Monitor the network through comprehensive analytics
        """)


def display_main_dashboard():
    """Display the main blockchain dashboard"""
    blockchain = st.session_state.blockchain
    current_user = st.session_state.current_user
    
    # Dashboard metrics
    display_dashboard_metrics()
    
    # Tabs for different functionalities
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🌐 Network", "💸 Transactions", "⛏️ Mining", 
        "📊 History", "🔗 Blockchain", "📈 Analytics"
    ])
    
    with tab1:
        display_network_overview()
    
    with tab2:
        display_transaction_interface()
    
    with tab3:
        display_mining_interface()
    
    with tab4:
        display_transaction_history()
    
    with tab5:
        display_blockchain_structure()
    
    with tab6:
        display_enhanced_analytics()


def display_dashboard_metrics():
    """Display dashboard metrics with cards"""
    blockchain = st.session_state.blockchain
    current_user = st.session_state.current_user
    stats = blockchain.get_blockchain_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        current_balance = blockchain.get_balance(current_user)
        st.metric("Your Balance", f"{current_balance:.2f}", "coins")
    
    with col2:
        zakat_fund = blockchain.get_balance('Zakat_Fund')
        st.metric("Zakat Fund", f"{zakat_fund:.2f}", "coins")
    
    with col3:
        st.metric("Total Nodes", stats['total_nodes'], "active")
    
    with col4:
        st.metric("Total Blocks", stats['total_blocks'], "mined")
    
    with col5:
        status_text = "✅ Valid" if stats['chain_valid'] else "❌ Invalid"
        st.metric("Chain Status", status_text, "integrity")


def display_network_overview():
    """Display network overview with all nodes"""
    st.markdown("### 🌐 Network Overview")
    
    blockchain = st.session_state.blockchain
    all_nodes = blockchain.get_all_nodes()
    
    if not all_nodes:
        st.warning("No nodes in the network yet.")
        return
    
    # Network statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Network Statistics")
        total_balance = sum(blockchain.balances.values())
        active_nodes = len([n for n in all_nodes.values() if n['is_active']])
        
        st.metric("Total Network Balance", f"{total_balance:.2f} coins")
        st.metric("Active Nodes", f"{active_nodes}/{len(all_nodes)}")
        st.metric("Total Transactions", sum(n['transactions_count'] for n in all_nodes.values()))
    
    with col2:
        st.markdown("#### 🎯 Zakat Overview")
        total_zakat_paid = sum(n['total_zakat_paid'] for n in all_nodes.values())
        total_zakat_received = sum(n['total_zakat_received'] for n in all_nodes.values())
        
        st.metric("Total Zakat Paid", f"{total_zakat_paid:.2f} coins")
        st.metric("Total Zakat Received", f"{total_zakat_received:.2f} coins")
        st.metric("Zakat Fund Balance", f"{blockchain.get_balance('Zakat_Fund'):.2f} coins")
    
    st.markdown("---")
    
    # Display all nodes using native Streamlit components
    st.markdown("#### 👥 All Network Nodes")
    
    for roll_number, node_info in all_nodes.items():
        current_balance = blockchain.get_balance(roll_number)
        is_current = roll_number == st.session_state.current_user
        is_creator = roll_number == st.session_state.creator_roll_number
        
        # Create a container for each node
        container = st.container()
        with container:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                badges = ""
                if is_creator:
                    badges += "👑 "
                if is_current:
                    badges += "🎯 "
                
                status = ""
                if is_creator and is_current:
                    status = "Creator & Current User"
                elif is_creator:
                    status = "Creator"
                elif is_current:
                    status = "Current User"
                else:
                    status = "Network Node"
                
                st.markdown(f"**{badges}{roll_number}**")
                st.caption(status)
            
            with col2:
                st.metric("Balance", f"{current_balance:.2f}", "coins")
            
            with col3:
                st.metric("Transactions", node_info['transactions_count'])
            
            with col4:
                st.metric("Zakat Paid", f"{node_info['total_zakat_paid']:.2f}")
            
            st.caption(f"Joined: {node_info['joined_at'][:10]}")
            
            if is_current:
                st.success("🎯 This is your current active account")
            
        st.markdown("---")


def display_transaction_interface():
    """Display enhanced transaction creation interface"""
    st.markdown("### 💸 Create Transactions")
    
    blockchain = st.session_state.blockchain
    current_user = st.session_state.current_user
    current_balance = blockchain.get_balance(current_user)
    
    # Display current user info using native components
    st.info(f"""
    **Current User:** {current_user}
    
    **Current Balance:** {current_balance:.2f} coins
    
    **Next Zakat Amount:** {blockchain.calculate_zakat(current_balance):.2f} coins (2.5%)
    """)
    
    # Transaction type selection
    transaction_type = st.radio(
        "Transaction Type",
        ["💰 Zakat Payment", "🔄 Transfer Coins", "🎁 Gift to Node"],
        help="Choose the type of transaction to create"
    )
    
    if transaction_type == "💰 Zakat Payment":
        display_zakat_interface(current_user, current_balance)
    elif transaction_type == "🔄 Transfer Coins":
        display_transfer_interface(current_user, current_balance)
    elif transaction_type == "🎁 Gift to Node":
        display_gift_interface(current_user, current_balance)


def display_zakat_interface(current_user, current_balance):
    """Display Zakat payment interface"""
    st.markdown("#### 💰 Zakat Payment (2.5% of your balance)")
    
    blockchain = st.session_state.blockchain
    zakat_amount = blockchain.calculate_zakat(current_balance)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("📊 Zakat Calculation")
        st.markdown(f"""
        **Current Balance:** {current_balance:.2f} coins
        
        **Zakat Rate:** 2.5% (Islamic requirement)
        
        **Zakat Amount:** {zakat_amount:.2f} coins
        
        **Remaining Balance:** {current_balance - zakat_amount:.2f} coins
        """)
    
    with col2:
        # Zakat recipient selection
        all_nodes = list(blockchain.get_all_nodes().keys())
        zakat_recipients = ["Zakat_Fund"] + [node for node in all_nodes if node != current_user]
        
        recipient = st.selectbox(
            "Zakat Recipient",
            zakat_recipients,
            help="Choose where to send the Zakat"
        )
        
        if st.button("💰 Pay Zakat", type="primary"):
            if zakat_amount > 0:
                success = blockchain.create_zakat_transaction(current_user, recipient)
                if success:
                    st.success(f"✅ Zakat transaction created! Amount: {zakat_amount:.2f} coins")
                    st.balloons()
                else:
                    st.error("❌ Failed to create Zakat transaction!")
            else:
                st.warning("⚠️ No Zakat amount to pay!")


def display_transfer_interface(current_user, current_balance):
    """Display transfer interface"""
    st.markdown("#### 🔄 Transfer Coins (with automatic Zakat deduction)")
    
    blockchain = st.session_state.blockchain
    all_nodes = [node for node in blockchain.get_all_nodes().keys() if node != current_user]
    
    col1, col2 = st.columns(2)
    
    with col1:
        recipient = st.selectbox(
            "Recipient",
            all_nodes + ["Custom Address"],
            help="Select recipient from network nodes or enter custom address"
        )
        
        if recipient == "Custom Address":
            custom_address = st.text_input("Enter Custom Address")
            recipient = custom_address if custom_address else ""
    
    with col2:
        amount = st.number_input(
            "Amount to Transfer",
            min_value=0.1,
            max_value=float(current_balance - blockchain.calculate_zakat(current_balance)),
            value=10.0,
            step=0.1,
            help="Amount of coins to transfer"
        )
    
    if recipient and amount > 0:
        zakat_amount = blockchain.calculate_zakat(current_balance)
        total_deduction = amount + zakat_amount
        
        st.markdown(f"""
        <div class="info-box">
            <h4>📊 Transaction Summary</h4>
            <p><strong>Transfer Amount:</strong> {amount:.2f} coins</p>
            <p><strong>Zakat Deduction:</strong> {zakat_amount:.2f} coins</p>
            <p><strong>Total Deduction:</strong> {total_deduction:.2f} coins</p>
            <p><strong>Remaining Balance:</strong> {current_balance - total_deduction:.2f} coins</p>
        </div>
        """, unsafe_allow_html=True)
        
        if total_deduction <= current_balance:
            if st.button("🔄 Send Transfer", type="primary"):
                success = blockchain.create_transfer_transaction(current_user, recipient, amount)
                if success:
                    st.success(f"✅ Transfer created! Sent {amount:.2f} coins to {recipient}")
                    st.balloons()
                else:
                    st.error("❌ Failed to create transfer!")
        else:
            st.error("❌ Insufficient balance!")


def display_gift_interface(current_user, current_balance):
    """Display gift interface (transfer without Zakat)"""
    st.markdown("#### 🎁 Gift to Node (special transfer)")
    
    blockchain = st.session_state.blockchain
    all_nodes = [node for node in blockchain.get_all_nodes().keys() if node != current_user]
    
    col1, col2 = st.columns(2)
    
    with col1:
        recipient = st.selectbox(
            "Gift Recipient",
            all_nodes,
            help="Select a network node to send a gift"
        )
    
    with col2:
        amount = st.number_input(
            "Gift Amount",
            min_value=1.0,
            max_value=float(current_balance * 0.1),  # Limit gifts to 10% of balance
            value=5.0,
            step=1.0,
            help="Amount to gift (limited to 10% of balance)"
        )
    
    if recipient and amount > 0:
        st.info(f"🎁 Sending {amount:.2f} coins as a gift to {recipient}")
        
        if st.button("🎁 Send Gift", type="primary"):
            # Create a special transaction with zero Zakat for gifts
            transaction = Transaction(
                sender=current_user,
                receiver=recipient,
                amount=amount,
                zakat_amount=0.0,  # No Zakat on gifts
                transaction_type="gift"
            )
            
            if blockchain.add_transaction(transaction):
                st.success(f"✅ Gift created! Sent {amount:.2f} coins to {recipient}")
                st.balloons()
            else:
                st.error("❌ Failed to create gift!")


def display_mining_interface():
    """Display enhanced mining interface"""
    st.markdown("### ⛏️ Mining Operations")
    
    blockchain = st.session_state.blockchain
    current_user = st.session_state.current_user
    pending_count = len(blockchain.pending_transactions)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Pending Transactions", pending_count)
    
    with col2:
        st.metric("Mining Reward", f"{blockchain.mining_reward} coins")
    
    with col3:
        mining_status = "🟢 Ready" if pending_count > 0 else "🟡 Waiting"
        st.metric("Mining Status", mining_status)
    
    # Display pending transactions
    if pending_count > 0:
        st.markdown("#### 📋 Pending Transactions")
        
        pending_data = []
        for i, tx in enumerate(blockchain.pending_transactions):
            pending_data.append({
                "#": i + 1,
                "From": tx.sender,
                "To": tx.receiver,
                "Amount": f"{tx.amount:.2f}",
                "Zakat": f"{tx.zakat_amount:.2f}",
                "Type": tx.transaction_type,
                "Time": tx.timestamp
            })
        
        df = pd.DataFrame(pending_data)
        st.dataframe(df, use_container_width=True)
        
        # Mining section
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <h4>⛏️ Mining Information</h4>
                <p><strong>Miner:</strong> {current_user}</p>
                <p><strong>Transactions to Process:</strong> {pending_count}</p>
                <p><strong>Mining Reward:</strong> {blockchain.mining_reward} coins</p>
                <p><strong>Estimated New Balance:</strong> {blockchain.get_balance(current_user) + blockchain.mining_reward:.2f} coins</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("⛏️ Mine Block", type="primary"):
                with st.spinner("⛏️ Mining block... Please wait..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)  # Simulate mining time
                        progress_bar.progress(i + 1)
                    
                    start_time = time.time()
                    blockchain.mine_pending_transactions(current_user)
                    end_time = time.time()
                    
                    st.success(f"🎉 Block mined successfully in {end_time - start_time:.2f} seconds!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
    else:
        st.markdown("""
        <div class="info-box">
            <h4>💡 No Pending Transactions</h4>
            <p>Create some transactions first, then return here to mine them into a block!</p>
            <p>All network nodes can participate in mining and earn rewards.</p>
        </div>
        """, unsafe_allow_html=True)


def display_transaction_history():
    """Display enhanced transaction history"""
    st.markdown("### 📊 Transaction History")
    
    blockchain = st.session_state.blockchain
    history = blockchain.get_transaction_history()
    
    if not history:
        st.info("📝 No transactions yet. Create some transactions to see history!")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tx_types = ["All"] + list(set(tx['transaction_type'] for tx in history))
        tx_type_filter = st.selectbox("Filter by Type", tx_types)
    
    with col2:
        blocks = ["All"] + [str(i) for i in sorted(set(tx['block_index'] for tx in history))]
        block_filter = st.selectbox("Filter by Block", blocks)
    
    with col3:
        users = ["All"] + list(set([tx['sender'] for tx in history] + [tx['receiver'] for tx in history]))
        user_filter = st.selectbox("Filter by User", users)
    
    # Apply filters
    filtered_history = history.copy()
    
    if tx_type_filter != "All":
        filtered_history = [tx for tx in filtered_history if tx['transaction_type'] == tx_type_filter]
    
    if block_filter != "All":
        filtered_history = [tx for tx in filtered_history if tx['block_index'] == int(block_filter)]
    
    if user_filter != "All":
        filtered_history = [tx for tx in filtered_history if tx['sender'] == user_filter or tx['receiver'] == user_filter]
    
    # Display results
    if filtered_history:
        df_data = []
        for tx in reversed(filtered_history):  # Show newest first
            df_data.append({
                "Block": tx['block_index'],
                "Time": tx['timestamp'][:16],  # Remove seconds
                "From": tx['sender'],
                "To": tx['receiver'], 
                "Amount": f"{tx['amount']:.2f}",
                "Zakat": f"{tx['zakat_amount']:.2f}",
                "Type": tx['transaction_type'].title()
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                csv,
                f"zakat_history_{st.session_state.creator_roll_number}.csv",
                "text/csv"
            )
        
        with col2:
            st.metric("Filtered Results", len(df_data))
    else:
        st.warning("🔍 No transactions match the selected filters.")


def display_blockchain_structure():
    """Display detailed blockchain structure"""
    st.markdown("### 🔗 Blockchain Structure")
    
    blockchain = st.session_state.blockchain
    
    # Chain validation status
    is_valid = blockchain.validate_chain()
    status_color = "#22c55e" if is_valid else "#ef4444"
    status_text = "✅ Valid & Secure" if is_valid else "❌ Integrity Compromised"
    
    st.markdown(f"""
    <div style="background: {'#ecfdf5' if is_valid else '#fef2f2'}; 
                border: 2px solid {status_color}; 
                border-radius: 0.75rem; 
                padding: 1.5rem; 
                text-align: center; 
                margin-bottom: 2rem;">
        <h3 style="color: {status_color}; margin: 0;">🔒 Blockchain Status: {status_text}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display blocks
    for block in reversed(blockchain.chain):  # Show newest first
        with st.expander(f"🧱 Block #{block.index} - {block.timestamp[:16]} ({len(block.transactions)} transactions)"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Block Details:**
                - **Index:** {block.index}
                - **Timestamp:** {block.timestamp}
                - **Nonce:** {block.nonce}
                - **Transactions:** {len(block.transactions)}
                """)
            
            with col2:
                st.markdown(f"""
                **Hash Information:**
                - **Seed (Roll Number):** `{block.roll_number}`
                - **Block Hash:** `{block.hash[:32]}...`
                - **Previous Hash:** `{block.previous_hash[:32]}...`
                - **Hash Valid:** {'✅' if block.hash == block.calculate_hash() else '❌'}
                """)
            
            # Display transactions in block
            if block.transactions:
                st.markdown("**Transactions in this block:**")
                tx_data = []
                for tx in block.transactions:
                    tx_data.append({
                        "From": tx.sender,
                        "To": tx.receiver,
                        "Amount": f"{tx.amount:.2f}",
                        "Zakat": f"{tx.zakat_amount:.2f}",
                        "Type": tx.transaction_type.title(),
                        "Time": tx.timestamp[:16]
                    })
                
                st.dataframe(pd.DataFrame(tx_data), use_container_width=True)


def display_enhanced_analytics():
    """Display enhanced analytics with interactive charts"""
    st.markdown("### 📈 Blockchain Analytics")
    
    blockchain = st.session_state.blockchain
    stats = blockchain.get_blockchain_stats()
    history = blockchain.get_transaction_history()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Blocks", stats['total_blocks'])
    with col2:
        st.metric("Total Transactions", stats['total_transactions'])
    with col3:
        st.metric("Total Zakat Collected", f"{stats['total_zakat_collected']:.2f}")
    with col4:
        st.metric("Network Nodes", stats['total_nodes'])
    
    # Charts section
    if history:
        col1, col2 = st.columns(2)
        
        with col1:
            # Balance distribution chart
            st.markdown("#### 💰 Account Balances")
            balance_data = {k: v for k, v in stats['balances'].items() if v > 0}
            
            if balance_data:
                fig = px.pie(
                    values=list(balance_data.values()),
                    names=list(balance_data.keys()),
                    title="Balance Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Transaction types chart
            st.markdown("#### 📊 Transaction Types")
            tx_types = {}
            for tx in history:
                tx_type = tx['transaction_type'].title()
                tx_types[tx_type] = tx_types.get(tx_type, 0) + 1
            
            if tx_types:
                fig = px.bar(
                    x=list(tx_types.keys()),
                    y=list(tx_types.values()),
                    title="Transaction Types Distribution",
                    color=list(tx_types.values()),
                    color_continuous_scale="Viridis"
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    # Node analysis
    st.markdown("#### 👥 Node Analysis")
    
    nodes_info = stats.get('nodes_info', {})
    if nodes_info:
        node_data = []
        for roll_number, info in nodes_info.items():
            node_data.append({
                "Node": roll_number,
                "Balance": blockchain.get_balance(roll_number),
                "Transactions": info['transactions_count'],
                "Zakat Paid": info['total_zakat_paid'],
                "Zakat Received": info['total_zakat_received'],
                "Join Date": info['joined_at'][:10],
                "Status": "🟢 Active" if info['is_active'] else "🔴 Inactive"
            })
        
        df = pd.DataFrame(node_data)
        st.dataframe(df, use_container_width=True)
    
    # Export section
    st.markdown("---")
    st.markdown("#### 📤 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Blockchain JSON"):
            blockchain_data = blockchain.to_dict()
            json_string = json.dumps(blockchain_data, indent=2)
            st.download_button(
                "📥 Download JSON",
                json_string,
                f"blockchain_{st.session_state.creator_roll_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )
    
    with col2:
        if history and st.button("📊 Export Analytics CSV"):
            analytics_data = []
            for tx in history:
                analytics_data.append({
                    "Date": tx['timestamp'][:10],
                    "Time": tx['timestamp'][11:16],
                    "Block": tx['block_index'],
                    "From": tx['sender'],
                    "To": tx['receiver'],
                    "Amount": tx['amount'],
                    "Zakat": tx['zakat_amount'],
                    "Type": tx['transaction_type'],
                    "Hash": tx.get('block_hash', '')[:16] + '...'
                })
            
            df = pd.DataFrame(analytics_data)
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                f"analytics_{st.session_state.creator_roll_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )
    
    with col3:
        if nodes_info and st.button("👥 Export Nodes Data"):
            nodes_csv = pd.DataFrame(node_data).to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                nodes_csv,
                f"nodes_{st.session_state.creator_roll_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )


def main():
    """Main application function"""
    st.set_page_config(
        page_title="Multi-Node Zakat Blockchain",
        page_icon="🕌",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    create_blockchain_interface()


if __name__ == "__main__":
    main()
