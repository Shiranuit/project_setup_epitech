#!/usr/bin/python3

## Author : Shiranuit ##

import os
import sys
import hashlib
import getpass
import subprocess
import re
import readline
import ast

def colored(txt, color):
    if (color.lower() == 'black'):
        color = '\x1B[30m'
    if (color.lower() == 'red'):
        color = '\x1B[31m'
    if (color.lower() == 'green'):
        color = '\x1B[32m'
    if (color.lower() == 'yellow'):
        color = '\x1B[33m'
    if (color.lower() == 'blue'):
        color = '\x1B[34m'
    if (color.lower() == 'magenta'):
        color = '\x1B[35m'
    if (color.lower() == 'cyan'):
        color = '\x1B[36m'
    if (color.lower() == 'white'):
        color = '\x1B[37m'
    return (color + txt + '\x1B[0m')

def cprint(txt, color):
    print(colored(txt, color));


def completer(table):
    def comp(text, state):
        options = [i for i in table if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp)

quit = False

def isError(stdout):
    out = stdout.decode('utf-8').split('\n')
    if len(out) > 1:
        if 'HTTP Error' in out[0]:
            regout = re.match(r"Error message : '(.+)'", out[1])
            if regout:
                return regout.group(1)

def check_token(user, token):
    result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'list'], stdout=subprocess.PIPE)
    if isError(result.stdout) and isError(result.stdout) == 'Bad token':
        return False
    else:
        return True

def loggin():
    user=""
    token=""
    while True:
        user = input("User: ")
        token = bytes(hashlib.sha512(bytes(getpass.getpass(), 'utf8')).hexdigest(), 'utf8')
        if check_token(user, token):
            break
        else:
            cprint('Wrong User or Password','red')
    return user, token

user, token = loggin()

def repo_list():
    result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'list'], stdout=subprocess.PIPE)
    if not isError(result.stdout):
        return [i for i in str(result.stdout.decode('utf-8')).split('\n') if len(i) > 0]

def prnt(stdout):
    out = isError(stdout)
    if out:
        cprint(out, 'red')
    else:
        cprint('\n'.join([str(i).replace("arthur.chaloin@epitech.eu", "arthur.chaloin@epitech.eu / Epitest") for i in stdout.decode('utf-8').split('\n') if len(i)>0]), 'green')

def repo_info(name):
    result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'info', name],stdout=subprocess.PIPE)
    out = isError(result.stdout)
    if out:
        cprint(out, 'red')
    else:
        dct = ast.literal_eval(result.stdout.decode('utf-8'))
        return dct

options=['Setup Repository', 'List Repositories', 'Delete Repository', 'Check Ramassage-tek Rights', 'Check Epitest Rights','Get Repository Access', 'Set Repository Access','Info Repository', 'Clone Repository', 'Change User']
mx = 0
for o in options:
    mx = max(mx, len(o)+6)

while not quit:
    print("╔"+"═"*mx+"╗")
    for i in range(len(options)):
        print("║["+str(i+1).zfill(2)+"] "+options[i]+" "*(mx-(len(options[i])+5))+"║")
    print("║[99] Exit"+" "*(mx-9)+"║")
    print("╚"+"═"*mx+"╝")
    try:
        action = int(input("> "))
    except Exception:
        action=0


    if action == 1:
        readline.set_completer(None)
        repo_name = input("Repository name: ")
        epitest = input("Want Epitest to access the repo (y/n): ")
        result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'create', repo_name], stdout=subprocess.PIPE)
        if not isError(result.stdout):
            prnt(result.stdout)
            result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'setacl', repo_name, 'ramassage-tek', 'r'],stdout=subprocess.PIPE)
            if not isError(result.stdout):
                prnt(result.stdout)
            else:
                prnt(result.stdout)
            if (epitest.lower() == "y" or epitest.lower() == "yes"):
                result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'setacl', repo_name, 'arthur.chaloin@epitech.eu', 'r'],stdout=subprocess.PIPE)
                if not isError(result.stdout):
                    prnt(result.stdout)
                    cprint("Epitest Rights added to the Repository", "yellow")
                else:
                    prnt(result.stdout)
            cprint('Done!', 'cyan')
        else:
            prnt(result.stdout)
    elif action == 2:
        for name in repo_list():
            cprint(name, 'green')
    elif action == 3:
        completer(repo_list())
        repo_name = input("Repository name: ")
        result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'delete', repo_name],stdout=subprocess.PIPE)
        prnt(result.stdout)
    elif action == 4:
        lst = repo_list()
        if lst:
            for repo_name in lst:
                result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'setacl', repo_name, 'ramassage-tek', 'r'],stdout=subprocess.PIPE)
                print('['+colored(isError(result.stdout) and 'X' or 'V', isError(result.stdout) and 'red' or 'green')+']'+colored(repo_name,'yellow'))
            cprint('Done! Everything is checked', 'cyan')
        else:
            cprint('Nothing can be checked', 'red')
    elif action == 5:
        lst = repo_list()
        if lst:
            for repo_name in lst:
                result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'setacl', repo_name, 'arthur.chaloin@epitech.eu', 'r'],stdout=subprocess.PIPE)
                print('['+colored(isError(result.stdout) and 'X' or 'V', isError(result.stdout) and 'red' or 'green')+']'+colored(repo_name,'yellow'))
            cprint('Done! Everything is checked', 'cyan')
        else:
            cprint('Nothing can be checked', 'red')
    elif action == 6:
        completer(repo_list())
        repo_name = input("Repository name: ")
        result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'getacl', repo_name],stdout=subprocess.PIPE)
        prnt(result.stdout)
    elif action == 7:
        completer(repo_list())
        repo_name = input("Repository name: ")
        readline.set_completer(None)
        user_name = input("User: ")
        rights = input('Rights (r-w-a): ')
        result = subprocess.run(['blih', '-u', user, '-t', token, 'repository', 'setacl', repo_name, user_name, rights],stdout=subprocess.PIPE)
        prnt(result.stdout)
    elif action == 8:
        completer(repo_list())
        repo_name = input("Repository name: ")
        data = repo_info(repo_name)
        if data:
            inmx = 0
            for k, v in data.items():
                inmx = max(inmx, len(k + " : " + v)+1)
            print("╔" + "═" * inmx + "╗")
            for k, v in data.items():
                print("║"+colored(k, 'yellow') + ' : ' + colored(v, 'cyan') +" "*(inmx-len(k + " : " + v)) + "║")
            print("╚" + "═" * inmx + "╝")
    elif action == 9:
        completer(repo_list())
        repo_name = input("Repository name: ")
        result = subprocess.run(['git', 'clone', 'git@git.epitech.eu:'+user+'/'+repo_name],stdout=subprocess.PIPE)
        prnt(result.stdout)
    elif action == len(options):
        user, token = loggin()
    elif action == 99:
        quit=True