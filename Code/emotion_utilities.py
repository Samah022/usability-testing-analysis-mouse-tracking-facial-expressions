number_happy_frames = 0
number_sad_frames = 0
number_angry_frames = 0
number_neutral_frames = 0
total_frames = 0


def get_emotion_probabilities(emotions):
    # Get the probabilities of happy, sad, angry, and neutral emotions from the first item in the emotions list
    happy_prob = emotions[0]['emotions'].get('happy', 0.0)
    sad_prob = emotions[0]['emotions'].get('sad', 0.0)
    angry_prob = emotions[0]['emotions'].get('angry', 0.0)
    neutral_prob = emotions[0]['emotions'].get('neutral', 0.0)
    
    return happy_prob, sad_prob, angry_prob, neutral_prob


def calculate_emotion_frames(happy_prob, sad_prob, angry_prob, neutral_prob ):
    global number_happy_frames, number_sad_frames, number_angry_frames, number_neutral_frames, total_frames

    # Update emotion frame counts based on the maximum probability among emotions
    if happy_prob > max(sad_prob, angry_prob, neutral_prob):
        number_happy_frames += 1
    if sad_prob > max(happy_prob, angry_prob, neutral_prob):
        number_sad_frames += 1
    if angry_prob > max(happy_prob, sad_prob, neutral_prob):
        number_angry_frames += 1
    if neutral_prob > max(happy_prob, sad_prob, angry_prob):
        number_neutral_frames += 1

    # Increment total frame count
    total_frames+=1

    return number_happy_frames, number_sad_frames, number_angry_frames, number_neutral_frames  


def calculate_emotion_percentages():
    # Calculate percentages of different emotions based on frame counts
    happy_percentage = (number_happy_frames / total_frames) * 100 if total_frames != 0 else 0
    sad_percentage = (number_sad_frames / total_frames) * 100 if total_frames != 0 else 0
    angry_percentage = (number_angry_frames / total_frames) * 100 if total_frames != 0 else 0
    neutral_percentage = (number_neutral_frames / total_frames) * 100 if total_frames != 0 else 0
    
    return happy_percentage, sad_percentage, angry_percentage, neutral_percentage


def display_emotion_percentage_table(happy_percentage, sad_percentage, angry_percentage, neutral_percentage):
    # Print header
    print("The following table shows the percentage of emotion of the user when he/she uses the system:")
    print("+------------+------------+")
    print("| Emotion    | Percentage |")
    print("+------------+------------+")

    # Print data rows
    print("| Happy      | {:>10.2f}% |".format(happy_percentage))
    print("| Sad        | {:>10.2f}% |".format(sad_percentage))
    print("| Angry      | {:>10.2f}% |".format(angry_percentage))
    print("| Neutral    | {:>10.2f}% |".format(neutral_percentage))

    # Print footer
    print("+------------+------------+")