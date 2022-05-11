if __name__ == '__main__':
    from subprocess import Popen, CREATE_NEW_CONSOLE

    # NX = ['CE12267']
    NX = ['CE12267', 'CE14323', 'CE25302']

    for nx in NX:
        p = Popen(f"c:/Users/david/Desktop/signal-scrapper/.venv/Scripts/python.exe bot_multi.py {nx}",
                  creationflags=CREATE_NEW_CONSOLE)
