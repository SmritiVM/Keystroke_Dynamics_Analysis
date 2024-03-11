from collections import defaultdict
from pynput.keyboard import Listener, Key
import csv
import time


def collect_keystroke_data():
    keystroke_timings = defaultdict(lambda : {'up':0, 'down':0})
    data_entered = ""
    backspaces = 0
    caps_lock = 0
    def on_press(key):
        nonlocal data_entered, backspaces, caps_lock
        if key == Key.backspace:
            data_entered = data_entered[:-1] #stripping last character
            backspaces += 1
        if key == Key.caps_lock:
            data_entered = data_entered[:-1] + data_entered[-1].upper()
            caps_lock += 1
                
        try:
            print(f'{key.char}')
            data_entered += key.char
            keystroke_timings[key.char]["down"] = time.time()
        except AttributeError:
            pass

    def on_release(key):
        try:
            keystroke_timings[key.char]["up"] = time.time()
        except AttributeError:
            pass
    
        if key == Key.enter:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    return data_entered, keystroke_timings, backspaces, caps_lock

def keyword(key):
    if key == '.': return 'period'
    if key == '5': return 'five'
    return key

def generate_timing_vector(keystroke_timings, password, backspaces, caps_lock, current_iteration, name):
    timing_vector = defaultdict(lambda: 0)
    # for key in keystroke_timings:
    #     print(key, keystroke_timings[key])

    # Iterating all characters of password and finding h, dd, ud
    '''
    Hold time = up - down
    DD = down - down_prev
    UD = down - up_prev
    '''
    timing_vector['name'] = name
    timing_vector['rep'] = current_iteration
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
    
    timing_vector['backspaces'] = backspaces
    timing_vector['caps_lock'] = caps_lock
    return timing_vector

def write_csv(name, timing_vectors):
    with open(f'{name}_keystrokes_bks.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(timing_vectors[0].keys()))
        writer.writeheader()
        writer.writerows(timing_vectors)
    


if __name__ == "__main__":
    name = input("Enter name: ")
    current_iteration = 1
    timing_vectors = []
    while current_iteration <= 10:
        data_entered, keystroke_timings, backspaces, caps_lock = collect_keystroke_data()
        password = ".tie5Ronal"
        if data_entered == password:
            print("Password correct!")
            timing_vector = generate_timing_vector(keystroke_timings, password, backspaces, caps_lock, current_iteration, name)
            timing_vectors.append(timing_vector)
            current_iteration += 1
        elif data_entered:
            print(data_entered)
            print("Incorrect! Enter again")
    
    write_csv(name, timing_vectors)
        
