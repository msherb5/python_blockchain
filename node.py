from uuid import uuid4

from blockchain import Blockchain
from verification import Verification



class Node:

    def __init__(self, ):
        #self.id = str(uuid4())
        self.id = 'Mike'
        self.blockchain = Blockchain(self.id)
       

    def get_transaction_value(self):
        user_amount = float(input('Your transaction amount please: '))
        user_recipient = input("your recipient's name please: ")
        return (user_recipient, user_amount)


    def get_user_choice(self):
        return int(input('Your choice: '))


    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print('Outputting block')
            print(block)
        else:
            print('-' * 20)


    def listen_for_input(self):

        waiting_for_input = True
        while waiting_for_input:
            print("please choose:")
            print('1: Add a new transaction value')
            print('2: Output values')
            print('3: Quit')
            print('5: Mine a new block')
            print('7: Check transaction validity')
            user_choice = self.get_user_choice()
            if user_choice == 1:
                tx_data = self.get_transaction_value()
                #tuple unpacking: takes the first element of tx_data and stores it in recipient, and stores the second element in amount
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount = amount):
                    print('Added Transaction')
                else:
                    print('Transaction failed')
            elif user_choice == 2:
                self.print_blockchain_elements()
            elif user_choice == 3:
                waiting_for_input = False
            elif user_choice == 5:
                self.blockchain.mine_block()
            elif user_choice == 7:

                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions valid')
                else:
                    print('There are invalid transactions') 
            else:
                print('input was invalid, please pick a value from the list ')
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_elements()
                print('invalid blockchain!!')
                break 
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))
        else:
            print('user done!')
        print('done')

node = Node()
node.listen_for_input()

    
    