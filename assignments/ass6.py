# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.
# 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.
# 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.
# 4) Adjust the logic to load the file content to work with pickled/ json data.

import json
import pickle

txtInput = input('Please enter the text you would like to write to a file: ')
input_list = txtInput.split()

#json version
# with open('file.txt', mode = 'w') as f:
#     f.write(json.dumps(input_list))

#pickle version
with open('file.p', mode = 'wb') as fp:
    fp.write(pickle.dumps(input_list))

choice = int(input('1: read the file contents, or 2: quit'))

if choice == 1:
    #json version
    # with open('file.txt', mode = 'r') as g:
    #     content = g.read()
    
    #pickle version
    with open('file.p', mode = 'rb') as gp:
        content = pickle.loads(gp.read())
    

    print(content)
else:
    quit()


