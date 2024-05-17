from mysql.connector import Error


def show_general_usability(conn):
    try:
        cursor = conn.cursor()

        # Query to count the number of users with task usability as 'easy' and 'difficult'
        cursor.execute("SELECT COUNT(*) FROM ai385project.usability_results WHERE task_usability = 'easy';")
        # Fetch the count of 'easy' task usability
        easy_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ai385project.usability_results WHERE task_usability = 'difficult';")
        # Fetch the count of 'difficult' task usability
        difficult_count = cursor.fetchone()[0]

        # Calculate total number of users
        total_count = easy_count + difficult_count

        # Calculate percentages
        easy_percentage = (easy_count / total_count) * 100 if total_count != 0 else 0
        difficult_percentage = (difficult_count / total_count) * 100 if total_count != 0 else 0

        # Print results in table format
        print("+------------+-----------------+")
        print("|    Task    |     Percentage  |")
        print("+------------+-----------------+")
        print("| Easy       |  {:>3} ({:>6.2f}%) |".format(easy_count, easy_percentage))
        print("| Difficult  |  {:>3} ({:>6.2f}%) |".format(difficult_count, difficult_percentage))
        print("+------------+-----------------+")

    except Error as e:
        print(e)

