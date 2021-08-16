#comment
from functools import reduce
import hashlib as hl
import json
import pickle


import utility.hash_util as hash_util
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet


#The reward we give miners for creating a block
MINING_REWARD = 10.0


class Blockchain:
    def __init__(self, hosting_node_id):
        #Starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        #Initializing our (empty) blockchain list
        self.chain = [genesis_block]
        #unhandled transactions
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:] 

    @chain.setter
    def chain(self, val):
        self.__chain = val


    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):

        try:
            with open('blockchain.txt', mode = 'r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                #print(file_content)
                

                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = [] 
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup!')

    def save_data(self):
        try:
            with open('blockchain.txt', mode = 'w') as f:  #wb would be writing binary data
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')


    def proof_of_work(self):
        last_bloc = self.__chain[-1]
        last_hash = hash_util.hash_block(last_bloc)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self):

        participant = self.hosting_node

        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        #calculate amount sent using reduce, first arg is lamda function with turnary if check, second arg is sender list, third arg is initial value
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

        tx_receiver = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum +  0, tx_receiver, 0)
        #return total balance
        return amount_received - amount_sent


    """ Doc string- used like a comment, comes up when hovering over the function name """
    def get_last_blockchain_value(self):

        if len(self.__chain) < 1:
            return None
        else:    
            return self.__chain[-1]


    def add_transaction(self, recipient, sender, signature, amount = 1.0): 
        # transaction = {
        #     'sender': sender, 
        #     'recipient': recipient, 
        #     'amount': amount
        # }

        if self.hosting_node == None:
            return False

        transaction = Transaction(sender, recipient, signature, amount)
        if not Wallet.verify_transaction(transaction):
            print('RIGHT HERE!!!')
            return False
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    #all open transactions put into a block, which is put into the blockchain
    def mine_block(self):

        if self.hosting_node == None:
            return False

        last_block = self.__chain[-1]
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        for tx in block_transactions:
            if not Wallet.verify_transaction(tx):
                return False
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True








