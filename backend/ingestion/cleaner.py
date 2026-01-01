import os

def clean_email(file_path):
    """
    Parses and cleans a single email file.
    TODO: Implement parsing for .eml/.msg
    """
    print(f"Processing {file_path}")
    pass

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(('.eml', '.msg', '.txt')):
                clean_email(os.path.join(root, file))

if __name__ == "__main__":
    # Example usage
    process_directory("../data/raw")
