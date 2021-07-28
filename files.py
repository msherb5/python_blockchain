with open('demo.txt', mode='r') as f:

    #f.write('Add this content!\n')

    # file_content = f.readlines()
    # f.close()
    # for line in file_content:
    #     print(line[:-1])

    # print(f.readline())
    line = f.readline()
    while line:
        print(line) 
        line = f.readline() 

print('Done!')




