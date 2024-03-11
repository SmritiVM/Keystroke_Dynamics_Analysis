from collections import defaultdict
from pynput.keyboard import Listener, Key
import csv
import time
import string

# Creating all 26x26 columns
features = {'H':0}
for letter1 in string.ascii_lowercase:
    for letter2 in string.ascii_lowercase:
        features[f'DD.{letter1}.{letter2}'] = 0
        features[f'UD.{letter1}.{letter2}'] = 0
# print(features)
        
counter = 1
def collect_keystroke_data():
    global counter
    keystroke_timings = defaultdict(lambda : {'key': '', 'up':0, 'down':0})
    backspaces = 0
    def on_press(key):
        global counter
        nonlocal backspaces
        if key == Key.space:
            return 
        if key == Key.backspace:
            backspaces += 1
        try:
            if not key.char.isalpha():
                return
            print(f'{key.char}')
            keystroke_timings[counter]['key'] = key.char
            keystroke_timings[counter]['down'] = time.time()
        except AttributeError:
            pass
    
    def on_release(key):
        global counter
        if key == Key.space:
            return 
        try:
            if not key.char.isalpha():
                return
            keystroke_timings[counter]['up'] = time.time()
        except AttributeError:
            pass
        counter += 1

        if key == Key.esc:
            return False
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    return keystroke_timings, backspaces

def generate_timing_vector(keystroke_timings, backspaces):
    global counter
    features['H'] += keystroke_timings[1]['up'] - keystroke_timings[1]['down']
    for i in range(2, counter):
        features['H'] += keystroke_timings[i]['up'] - keystroke_timings[i]['down']
        prev = keystroke_timings[i - 1]
        curr = keystroke_timings[i]
        prev_keyword = prev['key']
        curr_keyword = curr['key']
        features[f'DD.{prev_keyword}.{curr_keyword}'] = curr['down'] - prev['down']
        features[f'UD.{prev_keyword}.{curr_keyword}'] = curr['up'] - prev['down']
    features['backspaces'] = backspaces
    features['H'] = features['H']/counter

def write_csv(name, features):
    with open(f'{name}_keystrokes_26.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(features.keys()))
        writer.writeheader()
        writer.writerow(features)

if __name__ == "__main__":
    name = input("Enter name: ")
    keystroke_timings, backspaces = collect_keystroke_data()
    # print(keystroke_timings)
    generate_timing_vector(keystroke_timings, backspaces)
    # print(features)
    write_csv(name, features)
    
    
