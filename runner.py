if __name__ == '__main__':
    from subprocess import Popen, CREATE_NEW_CONSOLE

    # NX = ['CE12267']
    NX = ['CE14606', 'CE12267']

    for nx in NX:
        p = Popen(
            f"c:/Users/da.rodriguezh/Desktop/signal-scrapper/.venv/Scripts/python.exe bot.py {nx}")
        p.communicate()
