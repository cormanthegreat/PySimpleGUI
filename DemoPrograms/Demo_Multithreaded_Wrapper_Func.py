import threading
import time
import PySimpleGUI as sg

"""
    Performing function calls that are lengthy using a "wrapper function)

    This is one way to use threads and PySimpleGUI's write_event_value to enable users
        to call functions that would normally cause a GUI to appear hung.

    A helper function, perform_long_operation is used where a function call is normally done in your code.

    Instead of directly calling the function, a lambda is used and passed to the helper function along with
        the window that will receive the results and a key that is used to signal that the function
        has completed running.

    Copyright 2021 PySimpleGUI
"""

'''
M""""""""M dP                                        dP
Mmmm  mmmM 88                                        88
MMMM  MMMM 88d888b. 88d888b. .d8888b. .d8888b. .d888b88
MMMM  MMMM 88'  `88 88'  `88 88ooood8 88'  `88 88'  `88
MMMM  MMMM 88    88 88       88.  ... 88.  .88 88.  .88
MMMM  MMMM dP    dP dP       `88888P' `88888P8 `88888P8
MMMMMMMMMM
'''

def perform_long_operation(func, window, end_key):
    thread = threading.Thread(target=long_func_thread, args=(window, end_key, func))
    thread.start()


def long_func_thread(window: sg.Window, end_key, original_func):
    return_value = original_func()
    window.write_event_value(end_key,  return_value)


'''
M""MMMMM""M                            
M  MMMMM  M                            
M  MMMMM  M .d8888b. .d8888b. 88d888b. 
M  MMMMM  M Y8ooooo. 88ooood8 88'  `88 
M  `MMM'  M       88 88.  ... 88       
Mb       dM `88888P' `88888P' dP       
MMMMMMMMMMM                            
                                       
MM""""""""`M                            
MM  mmmmmmmM                            
M'      MMMM dP    dP 88d888b. .d8888b. 
MM  MMMMMMMM 88    88 88'  `88 88'  `"" 
MM  MMMMMMMM 88.  .88 88    88 88.  ... 
MM  MMMMMMMM `88888P' dP    dP `88888P' 
MMMMMMMMMMMM
'''


def my_long_func(count, a=1, b=2):
    """
    This is your function that takes a long time
    :param count:
    :param a:
    :param b:
    :return:
    """
    for i in range(count):
        print(i, a, b)
        time.sleep(.5)
    return 'DONE!'


'''
                    oo

88d8b.d8b. .d8888b. dP 88d888b.
88'`88'`88 88'  `88 88 88'  `88
88  88  88 88.  .88 88 88    88
dP  dP  dP `88888P8 dP dP    dP
'''


def main():
    layout = [  [sg.Text('Long running function call design pattern')],
                [sg.Text('How many times to run the loop?'), sg.Input(s=(4,1), key='-IN-')],
                [sg.Text(s=(30,1), k='-STATUS-')],
                [sg.Button('Go', bind_return_key=True), sg.Button('Exit')]  ]

    window = sg.Window('Window Title', layout)

    while True:             # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Go':
            window['-STATUS-'].update('Calling your function...')
            if values['-IN-'].isnumeric():
                # This is where the magic happens.  Add your function call as a lambda
                perform_long_operation(lambda : my_long_func(int(values['-IN-']), a=10),
                                       window, '-END KEY-')
            else:
                window['-STATUS-'].update('Try again... how about an int?')
        elif event == '-END KEY-':
            window['-STATUS-'].update(f'Completed. Returned: {values[event]}')
    window.close()

if __name__ == '__main__':
    main()
