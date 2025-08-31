"""
Test suite for Zakat Blockchain Simulation
Demonstrates all functionalities and validates implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blockchain import ZakatBlockchain, Transaction
import json


def test_blockchain_creation():
    """Test blockchain initialization"""
    print("=== Testing Blockchain Creation ===")
    
    roll_number = "2021-CS-001"
    blockchain = ZakatBlockchain(roll_number, 200.0)
    
    # Verify initialization
    assert len(blockchain.chain) == 1, "Genesis block should be created"
    assert blockchain.get_balance(roll_number) == 200.0, "Initial balance should be 200"
    assert blockchain.chain[0].roll_number == roll_number, "Roll number should be set correctly"
    
    print(f"✅ Blockchain created successfully for {roll_number}")
    print(f"✅ Initial balance: {blockchain.get_balance(roll_number)} coins")
    print(f"✅ Genesis block hash: {blockchain.chain[0].hash[:16]}...")
    print()
    
    return blockchain


def test_zakat_calculation():
    """Test Zakat calculation accuracy"""
    print("=== Testing Zakat Calculation ===")
    
    blockchain = ZakatBlockchain("2021-CS-002", 200.0)
    
    # Test different balance amounts
    test_cases = [
        (200.0, 5.0),    # 2.5% of 200
        (100.0, 2.5),    # 2.5% of 100
        (400.0, 10.0),   # 2.5% of 400
        (50.0, 1.25),    # 2.5% of 50
    ]
    
    for balance, expected_zakat in test_cases:
        calculated_zakat = blockchain.calculate_zakat(balance)
        assert calculated_zakat == expected_zakat, f"Zakat calculation failed for {balance}"
        print(f"✅ Balance: {balance} coins → Zakat: {calculated_zakat} coins")
    
    print()
    return blockchain


def test_transaction_creation():
    """Test transaction creation and validation"""
    print("=== Testing Transaction Creation ===")
    
    blockchain = ZakatBlockchain("2021-CS-003", 200.0)
    roll_number = "2021-CS-003"
    
    # Test Zakat transaction
    print("Creating Zakat transaction...")
    zakat_success = blockchain.create_zakat_transaction(roll_number)
    assert zakat_success, "Zakat transaction should be created successfully"
    assert len(blockchain.pending_transactions) == 1, "Should have 1 pending transaction"
    print("✅ Zakat transaction created successfully")
    
    # Test transfer transaction
    print("Creating transfer transaction...")
    transfer_success = blockchain.create_transfer_transaction(roll_number, "2021-CS-004", 50.0)
    assert transfer_success, "Transfer transaction should be created successfully"
    assert len(blockchain.pending_transactions) == 2, "Should have 2 pending transactions"
    print("✅ Transfer transaction created successfully")
    
    # Test invalid transaction (insufficient funds)
    print("Testing invalid transaction...")
    invalid_success = blockchain.create_transfer_transaction(roll_number, "2021-CS-005", 1000.0)
    assert not invalid_success, "Invalid transaction should fail"
    print("✅ Invalid transaction correctly rejected")
    
    print()
    return blockchain


def test_mining():
    """Test block mining functionality"""
    print("=== Testing Mining Functionality ===")
    
    blockchain = ZakatBlockchain("2021-CS-006", 200.0)
    roll_number = "2021-CS-006"
    
    # Create some transactions
    blockchain.create_zakat_transaction(roll_number)
    blockchain.create_transfer_transaction(roll_number, "2021-CS-007", 30.0)
    
    initial_blocks = len(blockchain.chain)
    initial_balance = blockchain.get_balance(roll_number)
    
    print(f"Before mining: {initial_blocks} blocks, balance: {initial_balance} coins")
    
    # Mine transactions
    blockchain.mine_pending_transactions(roll_number)
    
    final_blocks = len(blockchain.chain)
    final_balance = blockchain.get_balance(roll_number)
    
    print(f"After mining: {final_blocks} blocks, balance: {final_balance} coins")
    
    # Verify mining results
    assert final_blocks == initial_blocks + 1, "Should have one more block after mining"
    assert len(blockchain.pending_transactions) == 0, "No pending transactions after mining"
    assert final_balance > initial_balance - 35, "Balance should account for mining reward"
    
    print("✅ Mining completed successfully")
    print(f"✅ Mining reward received")
    print()
    
    return blockchain


def test_chain_validation():
    """Test blockchain validation and immutability"""
    print("=== Testing Chain Validation ===")
    
    blockchain = ZakatBlockchain("2021-CS-008", 200.0)
    roll_number = "2021-CS-008"
    
    # Create and mine some blocks
    for i in range(3):
        blockchain.create_transfer_transaction(roll_number, f"2021-CS-{9 + i}", 10.0)
        blockchain.mine_pending_transactions(roll_number)
    
    # Test valid chain
    is_valid = blockchain.validate_chain()
    assert is_valid, "Valid chain should pass validation"
    print("✅ Valid blockchain passes validation")
    
    # Test tampered chain (simulate tampering)
    original_hash = blockchain.chain[1].hash
    blockchain.chain[1].hash = "tampered_hash"
    
    is_valid_after_tampering = blockchain.validate_chain()
    assert not is_valid_after_tampering, "Tampered chain should fail validation"
    print("✅ Tampered blockchain correctly fails validation")
    
    # Restore original hash
    blockchain.chain[1].hash = original_hash
    
    is_valid_restored = blockchain.validate_chain()
    assert is_valid_restored, "Restored chain should pass validation"
    print("✅ Restored blockchain passes validation")
    
    print()
    return blockchain


def test_transaction_history():
    """Test transaction history and analytics"""
    print("=== Testing Transaction History ===")
    
    blockchain = ZakatBlockchain("2021-CS-010", 200.0)
    roll_number = "2021-CS-010"
    
    # Create various transactions
    transactions_created = 0
    
    # Zakat transactions
    blockchain.create_zakat_transaction(roll_number)
    transactions_created += 1
    
    # Transfer transactions
    blockchain.create_transfer_transaction(roll_number, "2021-CS-011", 25.0)
    transactions_created += 1
    
    blockchain.create_transfer_transaction(roll_number, "2021-CS-012", 15.0)
    transactions_created += 1
    
    # Mine transactions
    blockchain.mine_pending_transactions(roll_number)
    transactions_created += 1  # Mining reward transaction
    
    # Get transaction history
    history = blockchain.get_transaction_history()
    
    # Verify history (including genesis transaction)
    total_transactions = len(history)
    assert total_transactions >= transactions_created, "History should contain all transactions"
    print(f"✅ Transaction history contains {total_transactions} transactions")
    
    # Test statistics
    stats = blockchain.get_blockchain_stats()
    assert stats['total_blocks'] >= 2, "Should have multiple blocks"
    assert stats['total_zakat_collected'] > 0, "Should have collected some Zakat"
    assert stats['chain_valid'], "Chain should be valid"
    
    print(f"✅ Statistics: {stats['total_blocks']} blocks, {stats['total_transactions']} transactions")
    print(f"✅ Total Zakat collected: {stats['total_zakat_collected']:.2f} coins")
    
    print()
    return blockchain


def test_unique_hashing():
    """Test unique hashing with different roll numbers"""
    print("=== Testing Unique Hashing ===")
    
    # Create two blockchains with different roll numbers
    blockchain1 = ZakatBlockchain("2021-CS-100", 200.0)
    blockchain2 = ZakatBlockchain("2021-CS-200", 200.0)
    
    # Create identical transactions
    blockchain1.create_transfer_transaction("2021-CS-100", "recipient", 50.0)
    blockchain2.create_transfer_transaction("2021-CS-200", "recipient", 50.0)
    
    # Mine blocks
    blockchain1.mine_pending_transactions("2021-CS-100")
    blockchain2.mine_pending_transactions("2021-CS-200")
    
    # Compare hashes - they should be different due to different roll number seeds
    hash1 = blockchain1.chain[1].hash
    hash2 = blockchain2.chain[1].hash
    
    assert hash1 != hash2, "Hashes should be different with different roll number seeds"
    print(f"✅ Blockchain 1 hash: {hash1[:16]}...")
    print(f"✅ Blockchain 2 hash: {hash2[:16]}...")
    print("✅ Unique hashing verified with different roll numbers")
    
    print()


def test_balance_tracking():
    """Test accurate balance tracking across transactions"""
    print("=== Testing Balance Tracking ===")
    
    blockchain = ZakatBlockchain("2021-CS-300", 200.0)
    roll_number = "2021-CS-300"
    
    initial_balance = blockchain.get_balance(roll_number)
    print(f"Initial balance: {initial_balance} coins")
    
    # Create and mine multiple transactions
    transfers = [
        ("2021-CS-301", 30.0),
        ("2021-CS-302", 20.0),
        ("2021-CS-303", 25.0),
    ]
    
    expected_balance = initial_balance
    
    for recipient, amount in transfers:
        # Calculate expected deductions
        current_balance = blockchain.get_balance(roll_number)
        zakat = blockchain.calculate_zakat(current_balance)
        total_deduction = amount + zakat
        
        # Create transaction
        blockchain.create_transfer_transaction(roll_number, recipient, amount)
        blockchain.mine_pending_transactions(roll_number)
        
        # Update expected balance (deduction + mining reward)
        expected_balance = expected_balance - total_deduction + blockchain.mining_reward
        
        actual_balance = blockchain.get_balance(roll_number)
        print(f"Transfer {amount} to {recipient}: {actual_balance:.2f} coins (Zakat: {zakat:.2f})")
        
        # Allow for small floating point differences
        assert abs(actual_balance - expected_balance) < 0.01, f"Balance mismatch: expected {expected_balance}, got {actual_balance}"
    
    print("✅ Balance tracking accurate across all transactions")
    print()


def run_comprehensive_demo():
    """Run a comprehensive demonstration of all features"""
    print("=" * 60)
    print("COMPREHENSIVE ZAKAT BLOCKCHAIN DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Run all tests
    test_blockchain_creation()
    test_zakat_calculation()
    test_transaction_creation()
    test_mining()
    test_chain_validation()
    test_transaction_history()
    test_unique_hashing()
    test_balance_tracking()
    
    print("=" * 60)
    print("🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
    print("=" * 60)
    print()
    
    # Create a final demonstration blockchain
    print("=== Final Demonstration ===")
    demo_blockchain = ZakatBlockchain("DEMO-2021-CS-999", 200.0)
    
    # Simulate real-world usage
    print("Simulating real-world blockchain usage...")
    
    # Multiple users and transactions
    users = ["Student-A", "Student-B", "Student-C", "Zakat-Committee"]
    
    for i, user in enumerate(users):
        amount = 20 + (i * 10)
        demo_blockchain.create_transfer_transaction("DEMO-2021-CS-999", user, amount)
    
    # Pay Zakat
    demo_blockchain.create_zakat_transaction("DEMO-2021-CS-999")
    
    # Mine all transactions
    demo_blockchain.mine_pending_transactions("DEMO-2021-CS-999")
    
    # Display final statistics
    final_stats = demo_blockchain.get_blockchain_stats()
    print(f"\n📊 Final Blockchain Statistics:")
    print(f"   • Total Blocks: {final_stats['total_blocks']}")
    print(f"   • Total Transactions: {final_stats['total_transactions']}")
    print(f"   • Total Zakat Collected: {final_stats['total_zakat_collected']:.2f} coins")
    print(f"   • Chain Valid: {final_stats['chain_valid']}")
    print(f"   • Final Balance: {demo_blockchain.get_balance('DEMO-2021-CS-999'):.2f} coins")
    
    # Export blockchain data
    blockchain_data = demo_blockchain.to_dict()
    with open("demo_blockchain_export.json", "w") as f:
        json.dump(blockchain_data, f, indent=2)
    print(f"   • Blockchain exported to: demo_blockchain_export.json")
    
    print("\n🌟 Demonstration completed successfully!")
    print("🚀 Your Zakat Blockchain Simulation is ready to use!")


if __name__ == "__main__":
    run_comprehensive_demo()
