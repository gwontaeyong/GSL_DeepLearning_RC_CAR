import keyboard

def send_commend(*arg):

    data = ""
    for code in arg:
        data += code

    print(data)
    


if __name__ == "__main__":


    #연결 받기
    


    keyboard.add_hotkey('up', send_commend, args=('u'))
    keyboard.add_hotkey('down', send_commend, args=('d'))
    keyboard.add_hotkey('left', send_commend, args=('l'))
    keyboard.add_hotkey('right', send_commend, args=('r'))

    '''
    keyboard.add_hotkey('up+left', send_commend, args=('ul'))
    keyboard.add_hotkey('up+right', send_commend, args=('ur'))
    keyboard.add_hotkey('down+left', send_commend, args=('dl'))
    keyboard.add_hotkey('down+right', send_commend, args=('dr'))
    '''
    keyboard.wait()

    conn.close()


