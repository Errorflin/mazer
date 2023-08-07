from PIL import Image
import numpy as np

def convert_image_to_maze(input_image_path, output_maze_path):
    # Load the input image
    img = Image.open(input_image_path)
    img = img.convert('1')  # Convert to black and white image

    # Convert image to NumPy array
    maze_array = np.array(img)

    # Invert the array (1 for walls, 0 for paths)
    maze_array = 1 - maze_array

    # Map the array values to 'W' (wall) and '0' (path)
    maze_chars = np.where(maze_array, 'W', '0')

    # Convert NumPy array back to string representation
    maze_string = '\n'.join(''.join(row) for row in maze_chars)

    # Write the maze string to the output file
    with open(output_maze_path, 'w') as output_file:
        output_file.write(maze_string)

    print("Maze conversion completed successfully!")

if __name__ == "__main__":
    input_image_path = "input_maze.png"
    output_maze_path = input("Outuput maze path: ")
    convert_image_to_maze(input_image_path, output_maze_path)
