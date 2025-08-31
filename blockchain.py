"""
Zakat Blockchain Simulation
A complete blockchain implementation for Zakat calculation and distribution
Author: Student Implementation
Date: August 29, 2025
"""

import hashlib
import time
from datetime import datetime
from typing import List, Dict, Any, Optional


class Transaction:
    """
    Represents a single transaction in the blockchain
    """
    
    def __init__(self, sender: str, receiver: str, amount: float, 
                 zakat_amount: float, transaction_type: str, timestamp: str = None):
        """
        Initialize a new transaction
        
        Args:
            sender: Address/identifier of the sender
            receiver: Address/identifier of the receiver
            amount: Transaction amount
            zakat_amount: Zakat deducted (2.5% of balance)
            transaction_type: Type of transaction (zakat, transfer, etc.)
            timestamp: Transaction timestamp
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.zakat_amount = zakat_amount
        self.transaction_type = transaction_type
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary format"""
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'zakat_amount': self.zakat_amount,
            'transaction_type': self.transaction_type,
            'timestamp': self.timestamp
        }


class Block:
    """
    Represents a single block in the blockchain
    """
    
    def __init__(self, index: int, transactions: List[Transaction], 
                 previous_hash: str, roll_number: str):
        """
        Initialize a new block
        
        Args:
            index: Block index in the chain
            transactions: List of transactions in this block
            previous_hash: Hash of the previous block
            roll_number: Student's roll number (used as seed key)
        """
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.roll_number = roll_number
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate hash for the current block using roll number as seed
        
        Returns:
            Calculated hash string
        """
        # Create string representation of block data
        transactions_str = ""
        for tx in self.transactions:
            transactions_str += str(tx.to_dict())
        
        # Combine all block data with roll number as seed
        block_string = (
            f"{self.roll_number}:"  # Roll number as seed key
            f"{self.index}:"
            f"{transactions_str}:"
            f"{self.previous_hash}:"
            f"{self.timestamp}:"
            f"{self.nonce}"
        )
        
        # Generate hash using SHA-256
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2) -> None:
        """
        Mine the block with proof of work
        
        Args:
            difficulty: Mining difficulty (number of leading zeros)
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary format"""
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'roll_number': self.roll_number,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash
        }


class ZakatBlockchain:
    """
    Main blockchain class for Zakat simulation - Multi-node support
    """
    
    def __init__(self, creator_roll_number: str, initial_balance: float = 200.0):
        """
        Initialize the blockchain
        
        Args:
            creator_roll_number: Creator's roll number (seed key)
            initial_balance: Starting balance for the creator node
        """
        self.creator_roll_number = creator_roll_number
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.balances: Dict[str, float] = {creator_roll_number: initial_balance}
        self.nodes: Dict[str, Dict[str, Any]] = {}  # Store node information
        self.zakat_rate = 0.025  # 2.5% Zakat rate
        self.mining_reward = 10.0
        
        # Register creator as first node
        self.add_node(creator_roll_number, initial_balance)
        
        # Create genesis block
        self.create_genesis_block()
    
    def add_node(self, roll_number: str, initial_balance: float = 200.0) -> bool:
        """
        Add a new node to the blockchain network
        
        Args:
            roll_number: New node's roll number
            initial_balance: Starting balance for the new node
            
        Returns:
            True if node added successfully, False if already exists
        """
        if roll_number in self.nodes:
            return False
        
        self.nodes[roll_number] = {
            'roll_number': roll_number,
            'balance': initial_balance,
            'joined_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'transactions_count': 0,
            'total_zakat_paid': 0.0,
            'total_zakat_received': 0.0,
            'is_active': True
        }
        
        if roll_number not in self.balances:
            self.balances[roll_number] = initial_balance
        
        return True
    
    def get_all_nodes(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all nodes in the network"""
        return self.nodes.copy()
    
    def get_node_info(self, roll_number: str) -> Optional[Dict[str, Any]]:
        """Get specific node information"""
        return self.nodes.get(roll_number)
    
    def update_node_stats(self, roll_number: str, zakat_paid: float = 0.0, zakat_received: float = 0.0) -> None:
        """Update node statistics"""
        if roll_number in self.nodes:
            self.nodes[roll_number]['transactions_count'] += 1
            self.nodes[roll_number]['total_zakat_paid'] += zakat_paid
            self.nodes[roll_number]['total_zakat_received'] += zakat_received
            self.nodes[roll_number]['balance'] = self.get_balance(roll_number)

    def create_genesis_block(self) -> None:
        """Create the first block in the blockchain"""
        genesis_transaction = Transaction(
            sender="Genesis",
            receiver=self.creator_roll_number,
            amount=200.0,
            zakat_amount=0.0,
            transaction_type="genesis"
        )
        
        genesis_block = Block(
            index=0,
            transactions=[genesis_transaction],
            previous_hash="0",
            roll_number=self.creator_roll_number
        )
        
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def calculate_zakat(self, balance: float) -> float:
        """
        Calculate Zakat amount (2.5% of balance)
        
        Args:
            balance: Current balance
            
        Returns:
            Zakat amount to be deducted
        """
        return balance * self.zakat_rate
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """
        Add a new transaction to pending transactions
        
        Args:
            transaction: Transaction to add
            
        Returns:
            True if transaction is valid and added, False otherwise
        """
        # Validate transaction
        if not self.validate_transaction(transaction):
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def validate_transaction(self, transaction: Transaction) -> bool:
        """
        Validate a transaction
        
        Args:
            transaction: Transaction to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check if sender has sufficient balance
        sender_balance = self.get_balance(transaction.sender)
        total_amount = transaction.amount + transaction.zakat_amount
        
        if sender_balance < total_amount:
            return False
        
        return True
    
    def mine_pending_transactions(self, mining_address: str) -> None:
        """
        Mine all pending transactions and create a new block
        
        Args:
            mining_address: Address that will receive mining reward
        """
        # Add mining reward transaction
        reward_transaction = Transaction(
            sender="System",
            receiver=mining_address,
            amount=self.mining_reward,
            zakat_amount=0.0,
            transaction_type="mining_reward"
        )
        
        self.pending_transactions.append(reward_transaction)
        
        # Create new block with creator's roll number as seed
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash,
            roll_number=self.creator_roll_number  # Always use creator's roll number for consistency
        )
        
        # Mine the block
        block.mine_block()
        
        # Add block to chain
        self.chain.append(block)
        
        # Update balances
        self.update_balances(block)
        
        # Clear pending transactions
        self.pending_transactions = []
    
    def update_balances(self, block: Block) -> None:
        """
        Update account balances based on block transactions
        
        Args:
            block: Block containing transactions to process
        """
        for transaction in block.transactions:
            # Deduct from sender
            if transaction.sender != "System" and transaction.sender != "Genesis":
                if transaction.sender not in self.balances:
                    self.balances[transaction.sender] = 0.0
                
                total_deduction = transaction.amount + transaction.zakat_amount
                self.balances[transaction.sender] -= total_deduction
                
                # Update node stats
                self.update_node_stats(transaction.sender, zakat_paid=transaction.zakat_amount)
            
            # Add to receiver
            if transaction.receiver not in self.balances:
                self.balances[transaction.receiver] = 0.0
            
            self.balances[transaction.receiver] += transaction.amount
            
            # Update receiver stats for Zakat
            if transaction.transaction_type == "zakat" and transaction.receiver != "Zakat_Fund":
                self.update_node_stats(transaction.receiver, zakat_received=transaction.zakat_amount)
    
    def get_balance(self, address: str) -> float:
        """
        Get balance for a specific address
        
        Args:
            address: Address to check balance for
            
        Returns:
            Current balance
        """
        return self.balances.get(address, 0.0)
    
    def create_zakat_transaction(self, from_address: str, to_address: str = "Zakat_Fund") -> bool:
        """
        Create a Zakat transaction (2.5% deduction)
        
        Args:
            from_address: Address to deduct Zakat from
            to_address: Address to send Zakat to (default: Zakat_Fund)
            
        Returns:
            True if transaction created successfully, False otherwise
        """
        current_balance = self.get_balance(from_address)
        zakat_amount = self.calculate_zakat(current_balance)
        
        if zakat_amount > 0:
            transaction = Transaction(
                sender=from_address,
                receiver=to_address,
                amount=0.0,  # No transfer amount, just Zakat deduction
                zakat_amount=zakat_amount,
                transaction_type="zakat"
            )
            
            return self.add_transaction(transaction)
        
        return False
    
    def create_transfer_transaction(self, from_address: str, to_address: str, amount: float) -> bool:
        """
        Create a transfer transaction with automatic Zakat deduction
        
        Args:
            from_address: Sender address
            to_address: Receiver address
            amount: Amount to transfer
            
        Returns:
            True if transaction created successfully, False otherwise
        """
        current_balance = self.get_balance(from_address)
        zakat_amount = self.calculate_zakat(current_balance)
        
        transaction = Transaction(
            sender=from_address,
            receiver=to_address,
            amount=amount,
            zakat_amount=zakat_amount,
            transaction_type="transfer"
        )
        
        return self.add_transaction(transaction)
    
    def validate_chain(self) -> bool:
        """
        Validate the entire blockchain
        
        Returns:
            True if chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_transaction_history(self) -> List[Dict[str, Any]]:
        """
        Get complete transaction history from the blockchain
        
        Returns:
            List of all transactions in the blockchain
        """
        all_transactions = []
        
        for block in self.chain:
            for transaction in block.transactions:
                tx_dict = transaction.to_dict()
                tx_dict['block_index'] = block.index
                tx_dict['block_hash'] = block.hash
                all_transactions.append(tx_dict)
        
        return all_transactions
    
    def get_blockchain_stats(self) -> Dict[str, Any]:
        """
        Get blockchain statistics
        
        Returns:
            Dictionary containing blockchain statistics
        """
        total_zakat_collected = 0.0
        total_transactions = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                total_zakat_collected += transaction.zakat_amount
                total_transactions += 1
        
        return {
            'total_blocks': len(self.chain),
            'total_transactions': total_transactions,
            'total_zakat_collected': total_zakat_collected,
            'chain_valid': self.validate_chain(),
            'balances': self.balances.copy(),
            'creator_roll_number': self.creator_roll_number,
            'total_nodes': len(self.nodes),
            'active_nodes': len([n for n in self.nodes.values() if n['is_active']]),
            'nodes_info': self.nodes.copy()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire blockchain to dictionary format"""
        return {
            'creator_roll_number': self.creator_roll_number,
            'chain': [block.to_dict() for block in self.chain],
            'balances': self.balances,
            'nodes': self.nodes,
            'zakat_rate': self.zakat_rate,
            'stats': self.get_blockchain_stats()
        }


# Example usage and testing functions
def demo_blockchain():
    """Demonstrate blockchain functionality"""
    print("=== Zakat Blockchain Simulation Demo ===\n")
    
    # Create blockchain instance
    roll_number = "2021-CS-001"
    blockchain = ZakatBlockchain(roll_number)
    
    print(f"Created blockchain for student: {roll_number}")
    print(f"Initial balance: {blockchain.get_balance(roll_number)} coins\n")
    
    # Create some transactions
    print("Creating Zakat transaction...")
    blockchain.create_zakat_transaction(roll_number)
    
    print("Creating transfer transaction...")
    blockchain.create_transfer_transaction(roll_number, "2021-CS-002", 50.0)
    
    # Mine transactions
    print("\nMining pending transactions...")
    blockchain.mine_pending_transactions(roll_number)
    
    # Display results
    print(f"\nFinal balance: {blockchain.get_balance(roll_number)} coins")
    print(f"Zakat fund balance: {blockchain.get_balance('Zakat_Fund')} coins")
    print(f"Chain is valid: {blockchain.validate_chain()}")
    
    print("\n=== Blockchain Statistics ===")
    stats = blockchain.get_blockchain_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    demo_blockchain()
