# Dictionary to store counts of different task usability levels
task_usability_count_by_emotion = {'easy': 0, 'difficult': 0}

# Variable to store general usability of the system by emotion
task_usability_by_emotion = 'not defined'


def measure_usability_by_emotion(happy_prob, sad_prob, angry_prob, neutral_prob):
    # Update emotions data for "easy" and "difficult" emotions
    easy_prob = max(happy_prob, neutral_prob)
    difficult_prob = max(sad_prob, angry_prob)

    # Update emotion counts
    if easy_prob > difficult_prob:
        task_usability_count_by_emotion['easy'] += 1
    else:
        task_usability_count_by_emotion['difficult'] += 1


def determine_usability_by_emotion():
    # Determine usability by emotion
    if task_usability_count_by_emotion['easy'] > task_usability_count_by_emotion['difficult']:
        task_usability_by_emotion = 'easy'
        print("In general, this task was easy to do by the user.")

    elif task_usability_count_by_emotion['easy'] < task_usability_count_by_emotion['difficult']:
        task_usability_by_emotion = 'difficult'
        print("In general, this task was difficult to do by the user. The design flow of the task must be reconsidered.")

    else:
        task_usability_by_emotion = 'not defined'
        print("The system was unable to define the level.")

    return task_usability_by_emotion