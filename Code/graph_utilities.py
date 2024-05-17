import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Initialize Matplotlib figure and axes for the emotion graph:
# Create a new figure and axis
fig, ax = plt.subplots()

# Set the title of the plot
ax.set_title('Real-time Emotions Graph')

# Set the label for the x-axis
ax.set_xlabel('Time')

# Set the label for the y-axis
ax.set_ylabel('Probability')

# Initialize dictionaries to store usability data and plot lines
usability_level = {'easy': [], 'difficult': []}

# Dictionary to store plot lines for each usability level
lines = {level: ax.plot([], [], label=level)[0] for level in usability_level.keys()}

# Set the label for the y-axis
ax.legend()


def feed_graph(happy_prob, neutral_prob, sad_prob, angry_prob):

    # Calculate the probability for "easy" level
    easy_prob = max(happy_prob, neutral_prob)

    # Calculate the probability for "difficult" level
    difficult_prob = max(sad_prob, angry_prob)

    # Append data for "easy" level
    usability_level['easy'].append((time.time(), easy_prob))

    # Append data for "difficult" level
    usability_level['difficult'].append((time.time(), difficult_prob))


def update_graph():
    # Update the plot lines with the latest data
    # Iterate over each usability level's data
    for emo, data in usability_level.items():
        # Convert time to datetime objects
        x_data = [datetime.fromtimestamp(t) for t, _ in data]

        # Extract probability data
        x_data = [mdates.date2num(dt) for dt in x_data]
        y_data = [prob for _, prob in data]

        # Set data for the plot line
        lines[emo].set_data(x_data, y_data)

        # Recalculate the data limits for the axis
        ax.relim()

        # Autoscale the axis view
        ax.autoscale_view()

        # Redraw the plot
        plt.draw()

        # Pause to allow the plot to update
        plt.pause(0.01)