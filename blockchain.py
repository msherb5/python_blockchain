#comment
from functools import reduce
import hashlib as hl
import json
import pickle


import hash_util
from block import Block
from transaction import Transaction
from verification import Verification


MINING_REWARD = 10.0

blockchain = []
open_transactions = []
owner = 'Mike'

#curly braces without key value pairs is set notation

""" Doc string- used like a comment, comes up when hovering over the function name """
def get_last_blockchain_value():

    if len(blockchain) < 1:
        return None
    else:    
        return blockchain[-1]


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    #calculate amount sent using reduce, first arg is lamda function with turnary if check, second arg is sender list, third arg is initial value
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_receiver = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum +  0, tx_receiver, 0)

    return amount_received - amount_sent


def load_data():
    global blockchain
    global open_transactions

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
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        genesis_block = Block(0, '', [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print('Cleanup!')


load_data()

def save_data():
    try:
        with open('blockchain.txt', mode = 'w') as f:  #wb would be writing binary data
            saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed!')


def proof_of_work():
    last_bloc = blockchain[-1]
    last_hash = hash_util.hash_block(last_bloc)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def add_transaction( recipient, sender = owner, amount = 1.0): 
    # transaction = {
    #     'sender': sender, 
    #     'recipient': recipient, 
    #     'amount': amount
    # }
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False

#all open transactions put into a block, which is put into the blockchain
def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True



def get_transaction_value():
    user_amount = float(input('Your transaction amount please: '))
    user_recipient = input("your recipient's name please: ")
    return (user_recipient, user_amount)


def get_user_choice():
    return int(input('Your choice: '))


def print_blockchain_elements():
    for block in blockchain:
            print('Outputting block')
            print(block)
    else:
        print('-' * 20)


waiting_for_input = True

while waiting_for_input:
    print("please choose:")
    print('1: Add a new transaction value')
    print('2: Output values')
    print('3: Quit')
    print('5: Mine a new block')
    print('7: Check transaction validity')
    user_choice = get_user_choice()
    if user_choice == 1:
        tx_data = get_transaction_value()
        #tuple unpacking: takes the first element of tx_data and stores it in recipient, and stores the second element in amount
        recipient, amount = tx_data
        if add_transaction(recipient, amount = amount):
            print('Added Transaction')
        else:
            print('Transaction failed')
    elif user_choice == 2:
        print_blockchain_elements()
    elif user_choice == 3:
        waiting_for_input = False
    elif user_choice == 5:
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == 7:
        verifier = Verification()
        if verifier.verify_transactions(open_transactions, get_balance):
            print('All transactions valid')
        else:
            print('There are invalid transactions') 
    else:
        print('input was invalid, please pick a value from the list ')
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_blockchain_elements()
        print('invalid blockchain!!')
        break 
    print('Balance of {}: {:6.2f}'.format('Mike', get_balance('Mike')))
else:
    print('user done!')
print('done')