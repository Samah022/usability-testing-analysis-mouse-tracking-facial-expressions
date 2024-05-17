import pyautogui # install
import keyboard # install


def track_user_path():
    exit_key = keyboard.is_pressed('esc')
    prev_x = None
    prev_y = None

    # Open the file in write mode
    with open("mouse_positions.txt", "w") as file:
        while not exit_key:
            # Get the current mouse position
            x, y = pyautogui.position()

            # Check if the position has changed
            if x != prev_x or y != prev_y:
                # Write the coordinates to the file
                file.write(f"{x},{y}\n")
                prev_x = x
                prev_y = y

            exit_key = keyboard.is_pressed('esc')