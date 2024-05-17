from PIL import Image
from screeninfo import get_monitors #install


def generate_user_path():

    # Define the dimensions of the image to be the same of screen dimensions
    screen = get_monitors()[0]
    width, height = screen.width, screen.height

    # Create a new image with black pixels
    image = Image.new("L", (width, height), color=0)

    # Read the coordinates from the file
    with open("mouse_positions_referance.txt", "r") as file:
        coordinates = [tuple(map(int, line.strip().split(","))) for line in file]

    # Set the specified coordinates to white pixels
    for x, y in coordinates:
        image.putpixel((x, y), 255)

    # Save the image
    image.save("referance_image.png")