import argparse
import os

# Change all file extensions in input_directory to a single extension
# and output to output_directory

def main(input_directory, output_directory, ext_type):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    os.chdir(input_directory)
    
    for filename in os.listdir(input_directory):
        base = os.path.splitext(filename)[0]
        new_name = base + ext_type
        os.rename(filename, new_name)
        os.rename(input_directory + '\\' + new_name, output_directory + '\\' + new_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make all extensions the same')

    parser.add_argument("-o", "--output", type=str, default="output", help="The output directory")

    parser.add_argument("-i", "--input", type=str, help="The input directory")

    parser.add_argument("-t", "--type", type=str, help="Extension you want the files to be")

    args = vars(parser.parse_args())
    main(args["input"], args["output"], args["type"])
