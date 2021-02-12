import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))


def printWord(used, ans):
    print("Word:", end=" ")

    correct = 0
    for j in ans:
        if j in used:
            print(j, end=" ")
            correct+=1
        else:
            print("_", end=" ")

    print("\nMiss:", end=" ")

    for k in used:
        if k not in ans and k not in "1234567890":
            print(k, end=" ")

    print("\n")
    if correct == len(ans):
        print("You Win!!")


def hangman(n, li):
    if n.isdigit():
        n = int(n)
    if n == 6:
        print('------\n|\n|\n|\n|\\\n')
    elif n == 5:
        print('------\n|    O\n|\n|\n|\\\n')
    elif n == 4:
        print('------\n|    O\n|    |\n|\n|\\\n')
    elif n == 3:
        print('------\n|    O\n|   /|\n|\n|\\\n')
    elif n == 2:
        print('------\n|    O\n|   /|\\\n|\n|\\\n')
    elif n == 1:
        print('------\n|    O\n|   /|\\\n|   /\n|\\\n')
    elif n == 0:
        print('------\n|    O\n|   /|\\\n|   / \\\n|\\\n')
        print("You Lost!!")
    ans = li.pop()
    li.pop()
    printWord(li, ans)


status = 1
while status:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])
    for socks in read_sockets:
        # print(1)
        if socks == server:
            message = socks.recv(2048)
            encoding = 'utf-8'
            output = str(message, encoding)
            # print("out:", output)    # debug line
            notHaveNum = True
            for i in output:
                if i in "1234567890":
                    notHaveNum = False
                    break
            if notHaveNum or "." in output or ">>>" in output:
                # print(1)
                print(output)
            else:
                output = output.replace("'", "")
                output = output.replace("[", "")
                output = output.replace("]", "")
                output = output.replace(",", "")
                # print(output.split(" "))
                list_output = output.split(" ")
                hangman(list_output[len(list_output)-2], list_output)

            print("Type letter or 'exit' if you want to exit: ")
            # print(message)
        else:
            # print("Type letter or 'exit' if you want to exit: ", end="")
            message = sys.stdin.readline()
            if "exit" in message:
                status = 0
            server.send(str.encode(str(message)))
            sys.stdout.write("<You>: ")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()
