import time

def read_values(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        values = [float(value) for line in lines for value in line.split()]
    return values

def calculate_average(values1, values2):
    averages = [(val1 + val2) / 2 for val1, val2 in zip(values1, values2)]
    return averages

file1_path = 'D:\\Final Project\\Text\\Final Output\\speech_last_prediction.txt'  
file2_path = 'D:\\Final Project\\Text\\Final Output\\face_last_prediction.txt'  

while True:
    values1 = read_values(file1_path)
    values2 = read_values(file2_path)

    averages = calculate_average(values1, values2)

    # Find the position of the greatest value
    greatest_position = averages.index(max(averages)) + 1  # Adding 1 to get 1-based position

    # Write the greatest position to a text file
    output_file_path = 'D:\\Final Project\\Text\\Final Output\\greatest_position.txt'
    with open(output_file_path, 'w') as output_file:
        output_file.write(str(greatest_position))

    print(f"The position of the greatest value ({max(averages):.4f}) is: {greatest_position}")

    # Wait for 10 seconds before the next iteration
    time.sleep(10)
