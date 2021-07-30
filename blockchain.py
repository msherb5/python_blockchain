#comment
from functools import reduce
import hashlib as hl
import json
from collections import OrderedDict
import pickle


import hash_util


MINING_REWARD = 10.0

blockchain = []
open_transactions = []
owner = 'Mike'

#curly braces without key value pairs is set notation
participants = {'Mike',}

""" Doc string- used like a comment, comes up when hovering over the function name """
def get_last_blockchain_value():

    if len(blockchain) < 1:
        return None
    else:    
        return blockchain[-1]


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    #calculate amount sent using reduce, first arg is lamda function with turnary if check, second arg is sender list, third arg is initial value
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_receiver = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
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
                updated_block = {
                    'previous_hash': block['previous_hash'],
                    'index': block['index'],
                    'proof': block['proof'],
                    'transactions': [OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
                }
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except IOError:
        genesis_block = {
            'previous_hash': '',
            'index': 0,
            'transactions': [],
            'proof': 100
        }
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print('Cleanup!')


load_data()


def save_data():
    try:
        with open('blockchain.txt', mode = 'w') as f:  #wb would be writing binary data
            f.write(json.dumps(blockchain))
            f.write('\n')
            f.write(json.dumps(open_transactions))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed!')


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    print(guess)
    guess_hash = hash_util.hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_bloc = blockchain[-1]
    last_hash = hash_util.hash_block(last_bloc)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']
     


def add_transaction( recipient, sender = owner, amount = 1.0): 
    # transaction = {
    #     'sender': sender, 
    #     'recipient': recipient, 
    #     'amount': amount
    # }

    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
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
    reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
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


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_util.hash_block(blockchain[index-1]):
            return False
        #range selector excludes reward transaction
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid!')
            return False
    return True


def verify_transactions():
        return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print("please choose:")
    print('1: Add a new transaction value')
    print('2: Output values')
    print('3: Quit')
    print('4: manipulate the chain')
    print('5: Mine a new block')
    print("6: outpit participant list")
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
    elif user_choice == 4:
        if len(blockchain) >= 1:
            blockchain[0] = {
            'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Max', 'amount': 100.0}]
            }
    elif user_choice == 5:
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == 6:
       print(participants)
    elif user_choice == 7:
        if verify_transactions():
            print('All transactions valid')
        else:
            print('There are invalid transactions') 
    else:
        print('input was invalid, please pick a value from the list ')
    if not verify_chain():
        print_blockchain_elements()
        print('invalid blockchain!!')
        break 
    print('Balance of {}: {:6.2f}'.format('Mike', get_balance('Mike')))
else:
    print('user done!')
print('done')