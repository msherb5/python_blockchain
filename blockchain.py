#comment

MINING_REWARD = 10.0

genesis_block = {
    'previous_hash': '',
        'index': 0,
        'transactions': []
}
blockchain = [genesis_block]
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
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_receiver = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_receiver:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']
     


def add_transaction( recipient, sender = owner, amount = 1.0): 
    transaction = {
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

def hash_block(block):
    #join syntax to change printing from looking like a list, to a string connected by dashes
    return '-'.join([str(block[key]) for key in block])


#all open transactions put into a block, which is put into the blockchain
def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
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
        if block['previous_hash'] != hash_block(blockchain[index-1]):
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
    print(get_balance('Mike'))
else:
    print('user done!')
print('done')