from collections import defaultdict
from pynput.keyboard import Listener, Key
import csv
import time

# keystroke_data = []


def collect_keystroke_data():
    keystroke_timings = defaultdict(lambda : {'up':0, 'down':0})
    data_entered = ""
    def on_press(key):
        nonlocal data_entered
        
        # if key == Key.backspace:
        #     data_entered = data_entered[:-1] #stripping last character
        # if key == Key.shift:
        #     keystroke_timings['Shift']['down'] = time.time()
        #     return 
        try:
            print(f'{key.char}')
            data_entered += key.char
            keystroke_timings[key.char]["down"] = time.time()
        except AttributeError:
            pass

    def on_release(key):
        # if key == Key.shift:
        #     keystroke_timings['Shift']['up'] = time.time()
        #     return
        try:
            keystroke_timings[key.char]["up"] = time.time()
        except AttributeError:
            pass
        if key == Key.esc:
            # Write data to CSV file
            # with open("keystroke_data.csv", mode="w", newline="") as file:
            #     writer = csv.DictWriter(file, fieldnames=["key", "hold_time", "down_down_time", "up_down_time"])
            #     writer.writeheader()
            #     for data in keystroke_data:
            #         writer.writerow(data)
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    return data_entered, keystroke_timings

def keyword(key):
    if key == '.': return 'period'
    if key == '5': return 'five'
    return key

def generate_timing_vector(keystroke_timings, password):
    timing_vector = defaultdict(lambda: 0)
    # # First drop any keys stored which do not belong to the password
    # # and count the number of backspaces
    # backspaces = 0
    # required_keys = []
    for key in keystroke_timings:
        print(key, keystroke_timings[key])

    # Iterating all characters of password and finding h, dd, ud
    # Hold time = up - down
    # DD = down - down_prev
    # UD = down - up_prev
    prev = None
    for index, key in enumerate(password):
        curr_keyword = keyword(key)
        prev_keyword = keyword(prev)
        # Hold time
        timing_vector[f'H.{curr_keyword}'] = keystroke_timings[key]['up'] - keystroke_timings[key]['down']
        if index == 0:
            prev = key
            continue
        # DD
        timing_vector[f'DD.{prev_keyword}.{curr_keyword}'] = keystroke_timings[key]['down'] - keystroke_timings[prev]['down']
        # UD
        timing_vector[f'UD.{prev_keyword}.{curr_keyword}'] = keystroke_timings[key]['up'] - keystroke_timings[prev]['down']
        prev = key
    
    print(timing_vector)

if __name__ == "__main__":
    data_entered, keystroke_timings = collect_keystroke_data()
    # print(data_entered)
    # for key in keystroke_timings:
    #     print(key, keystroke_timings[key])
    password = ".tie5Ronal"
    if data_entered == password:
        generate_timing_vector(keystroke_timings, password)
    else:
        print("Incorrect")
        
