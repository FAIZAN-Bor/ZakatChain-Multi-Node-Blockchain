"""
Multi-Node Test Suite for Enhanced Zakat Blockchain Simulation
Tests all multi-node functionality and enhanced features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blockchain import ZakatBlockchain, Transaction
import json


def test_multi_node_creation():
    """Test multi-node blockchain creation and management"""
    print("=== Testing Multi-Node Creation ===")
    
    # Create blockchain with creator
    creator = "2021-CS-001"
    blockchain = ZakatBlockchain(creator, 200.0)
    
    assert len(blockchain.get_all_nodes()) == 1, "Should start with creator node"
    print(f"✅ Creator node created: {creator}")
    
    # Add multiple nodes
    nodes_to_add = [
        ("2021-CS-002", 200.0),
        ("2021-CS-003", 150.0),
        ("2021-CS-004", 250.0),
        ("2021-CS-005", 180.0)
    ]
    
    for roll_number, balance in nodes_to_add:
        success = blockchain.add_node(roll_number, balance)
        assert success, f"Should successfully add node {roll_number}"
        assert blockchain.get_balance(roll_number) == balance, f"Node {roll_number} should have correct balance"
        print(f"✅ Added node: {roll_number} with {balance} coins")
    
    # Test duplicate node addition
    duplicate_success = blockchain.add_node("2021-CS-002", 100.0)
    assert not duplicate_success, "Should not allow duplicate nodes"
    print("✅ Duplicate node addition correctly rejected")
    
    # Verify all nodes exist
    all_nodes = blockchain.get_all_nodes()
    assert len(all_nodes) == 5, "Should have 5 nodes total"
    print(f"✅ Total nodes in network: {len(all_nodes)}")
    
    print()
    return blockchain


def test_multi_node_transactions():
    """Test transactions between multiple nodes"""
    print("=== Testing Multi-Node Transactions ===")
    
    # Create blockchain with multiple nodes
    blockchain = test_multi_node_creation()
    
    # Test transactions between different nodes
    transactions = [
        ("2021-CS-001", "2021-CS-002", 30.0, "transfer"),
        ("2021-CS-002", "2021-CS-003", 20.0, "transfer"),
        ("2021-CS-003", "2021-CS-004", 15.0, "transfer"),
        ("2021-CS-004", "2021-CS-005", 25.0, "transfer"),
    ]
    
    print("Creating transactions between nodes...")
    for sender, receiver, amount, tx_type in transactions:
        if tx_type == "transfer":
            success = blockchain.create_transfer_transaction(sender, receiver, amount)
            assert success, f"Transaction from {sender} to {receiver} should succeed"
            print(f"✅ Transfer: {sender} → {receiver}: {amount} coins")
    
    # Test Zakat transactions
    print("\nCreating Zakat transactions...")
    for node in ["2021-CS-001", "2021-CS-002", "2021-CS-003"]:
        zakat_success = blockchain.create_zakat_transaction(node, "Zakat_Fund")
        assert zakat_success, f"Zakat transaction for {node} should succeed"
        print(f"✅ Zakat payment from {node}")
    
    # Verify pending transactions
    pending_count = len(blockchain.pending_transactions)
    assert pending_count > 0, "Should have pending transactions"
    print(f"✅ Pending transactions: {pending_count}")
    
    print()
    return blockchain


def test_multi_node_mining():
    """Test mining with multiple nodes"""
    print("=== Testing Multi-Node Mining ===")
    
    # Get blockchain with pending transactions
    blockchain = test_multi_node_transactions()
    
    # Different nodes can mine
    miners = ["2021-CS-001", "2021-CS-003", "2021-CS-005"]
    
    for i, miner in enumerate(miners):
        if len(blockchain.pending_transactions) > 0:
            initial_balance = blockchain.get_balance(miner)
            blockchain.mine_pending_transactions(miner)
            final_balance = blockchain.get_balance(miner)
            
            # Miner should receive reward
            assert final_balance > initial_balance, f"Miner {miner} should receive reward"
            print(f"✅ Block mined by {miner}, reward: {final_balance - initial_balance:.2f} coins")
        
        # Create more transactions for next mining round
        if i < len(miners) - 1:
            blockchain.create_transfer_transaction(miner, miners[(i + 1) % len(miners)], 10.0)
    
    print()
    return blockchain


def test_node_statistics():
    """Test node statistics and analytics"""
    print("=== Testing Node Statistics ===")
    
    blockchain = test_multi_node_mining()
    stats = blockchain.get_blockchain_stats()
    
    # Verify statistics
    assert stats['total_nodes'] >= 5, "Should have at least 5 nodes"
    assert stats['active_nodes'] >= 5, "All nodes should be active"
    assert stats['total_blocks'] > 1, "Should have mined blocks"
    assert stats['total_transactions'] > 0, "Should have transactions"
    assert stats['total_zakat_collected'] > 0, "Should have collected Zakat"
    
    print(f"✅ Total nodes: {stats['total_nodes']}")
    print(f"✅ Active nodes: {stats['active_nodes']}")
    print(f"✅ Total blocks: {stats['total_blocks']}")
    print(f"✅ Total transactions: {stats['total_transactions']}")
    print(f"✅ Total Zakat collected: {stats['total_zakat_collected']:.2f}")
    
    # Check individual node statistics
    nodes_info = stats['nodes_info']
    for roll_number, node_info in nodes_info.items():
        print(f"✅ {roll_number}: {node_info['transactions_count']} transactions, "
              f"{node_info['total_zakat_paid']:.2f} Zakat paid")
    
    print()
    return blockchain


def test_balance_distribution():
    """Test balance distribution across nodes"""
    print("=== Testing Balance Distribution ===")
    
    blockchain = test_node_statistics()
    
    # Check balance distribution
    total_balance = 0
    print("Final balance distribution:")
    
    for node in blockchain.get_all_nodes().keys():
        balance = blockchain.get_balance(node)
        total_balance += balance
        print(f"  {node}: {balance:.2f} coins")
    
    zakat_fund = blockchain.get_balance('Zakat_Fund')
    total_balance += zakat_fund
    print(f"  Zakat_Fund: {zakat_fund:.2f} coins")
    print(f"Total network balance: {total_balance:.2f} coins")
    
    # Verify conservation of coins (accounting for mining rewards)
    initial_total = 5 * 200  # 5 nodes with 200 coins each
    blocks_mined = len(blockchain.chain) - 1  # Exclude genesis block
    expected_total = initial_total + (blocks_mined * blockchain.mining_reward)
    
    assert abs(total_balance - expected_total) < 0.01, "Balance should be conserved"
    print(f"✅ Balance conservation verified: {total_balance:.2f} ≈ {expected_total:.2f}")
    
    print()
    return blockchain


def test_gift_transactions():
    """Test gift transactions (no Zakat deduction)"""
    print("=== Testing Gift Transactions ===")
    
    blockchain = test_balance_distribution()
    
    # Create gift transactions
    gifts = [
        ("2021-CS-001", "2021-CS-002", 5.0),
        ("2021-CS-003", "2021-CS-004", 8.0),
        ("2021-CS-005", "2021-CS-001", 3.0),
    ]
    
    for sender, receiver, amount in gifts:
        # Create gift transaction manually (no Zakat)
        gift_tx = Transaction(
            sender=sender,
            receiver=receiver,
            amount=amount,
            zakat_amount=0.0,
            transaction_type="gift"
        )
        
        success = blockchain.add_transaction(gift_tx)
        assert success, f"Gift from {sender} to {receiver} should succeed"
        print(f"✅ Gift: {sender} → {receiver}: {amount} coins (no Zakat)")
    
    # Mine gift transactions
    blockchain.mine_pending_transactions("2021-CS-002")
    print("✅ Gift transactions mined successfully")
    
    print()
    return blockchain


def test_blockchain_export():
    """Test blockchain data export functionality"""
    print("=== Testing Blockchain Export ===")
    
    blockchain = test_gift_transactions()
    
    # Export complete blockchain
    blockchain_data = blockchain.to_dict()
    
    # Verify export structure
    required_keys = ['creator_roll_number', 'chain', 'balances', 'nodes', 'zakat_rate', 'stats']
    for key in required_keys:
        assert key in blockchain_data, f"Export should contain {key}"
    
    print("✅ Blockchain export structure verified")
    
    # Save to file
    export_filename = "multi_node_blockchain_test.json"
    with open(export_filename, 'w') as f:
        json.dump(blockchain_data, f, indent=2)
    
    print(f"✅ Blockchain exported to {export_filename}")
    
    # Verify file size and content
    file_size = os.path.getsize(export_filename)
    assert file_size > 1000, "Export file should be substantial"
    print(f"✅ Export file size: {file_size} bytes")
    
    print()
    return blockchain


def test_chain_integrity():
    """Test blockchain integrity with multiple nodes"""
    print("=== Testing Chain Integrity ===")
    
    blockchain = test_blockchain_export()
    
    # Verify chain integrity
    is_valid = blockchain.validate_chain()
    assert is_valid, "Blockchain should be valid"
    print("✅ Blockchain integrity verified")
    
    # Test tampering detection
    if len(blockchain.chain) > 2:
        original_hash = blockchain.chain[1].hash
        blockchain.chain[1].hash = "tampered_hash_12345"
        
        is_valid_after_tampering = blockchain.validate_chain()
        assert not is_valid_after_tampering, "Tampered blockchain should be invalid"
        print("✅ Tampering detection working")
        
        # Restore original hash
        blockchain.chain[1].hash = original_hash
        is_valid_restored = blockchain.validate_chain()
        assert is_valid_restored, "Restored blockchain should be valid"
        print("✅ Chain restoration working")
    
    print()
    return blockchain


def run_multi_node_demo():
    """Run comprehensive multi-node demonstration"""
    print("=" * 70)
    print("MULTI-NODE ZAKAT BLOCKCHAIN COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Run all tests
    test_multi_node_creation()
    test_multi_node_transactions()
    test_multi_node_mining()
    test_node_statistics()
    test_balance_distribution()
    test_gift_transactions()
    test_blockchain_export()
    final_blockchain = test_chain_integrity()
    
    print("=" * 70)
    print("🎉 ALL MULTI-NODE TESTS PASSED SUCCESSFULLY! 🎉")
    print("=" * 70)
    print()
    
    # Final demonstration summary
    print("=== Final Multi-Node Network Summary ===")
    final_stats = final_blockchain.get_blockchain_stats()
    
    print(f"📊 Network Statistics:")
    print(f"   • Creator: {final_blockchain.creator_roll_number}")
    print(f"   • Total Nodes: {final_stats['total_nodes']}")
    print(f"   • Active Nodes: {final_stats['active_nodes']}")
    print(f"   • Total Blocks: {final_stats['total_blocks']}")
    print(f"   • Total Transactions: {final_stats['total_transactions']}")
    print(f"   • Total Zakat Collected: {final_stats['total_zakat_collected']:.2f} coins")
    print(f"   • Chain Valid: {final_stats['chain_valid']}")
    
    print(f"\n💰 Final Node Balances:")
    for node in final_blockchain.get_all_nodes().keys():
        balance = final_blockchain.get_balance(node)
        node_info = final_blockchain.get_node_info(node)
        print(f"   • {node}: {balance:.2f} coins "
              f"({node_info['transactions_count']} transactions, "
              f"{node_info['total_zakat_paid']:.2f} Zakat paid)")
    
    zakat_fund = final_blockchain.get_balance('Zakat_Fund')
    print(f"   • Zakat_Fund: {zakat_fund:.2f} coins")
    
    print(f"\n🌟 Enhanced Features Demonstrated:")
    print("   ✅ Multi-node network creation and management")
    print("   ✅ Cross-node transactions with automatic Zakat")
    print("   ✅ Collaborative mining by different nodes")
    print("   ✅ Gift transactions without Zakat deduction")
    print("   ✅ Comprehensive node statistics tracking")
    print("   ✅ Balance conservation across network")
    print("   ✅ Blockchain integrity and tamper detection")
    print("   ✅ Complete data export functionality")
    
    print(f"\n🚀 Your Enhanced Multi-Node Zakat Blockchain is ready!")
    print("   • Professional UI with proper color scheme")
    print("   • Interactive analytics and visualizations")
    print("   • Real-time node management capabilities")
    print("   • Comprehensive transaction history")
    print("   • Advanced blockchain explorer")


if __name__ == "__main__":
    run_multi_node_demo()
