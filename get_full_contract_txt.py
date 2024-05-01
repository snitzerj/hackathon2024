def get_full_contract_text(filename):
    file_path = f'data/full_contract_txt/{filename}'
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            print("File found")
            return file_contents
    except FileNotFoundError:
        print("File not found.")
        return None
    except IOError:
        print("Error reading the file.")