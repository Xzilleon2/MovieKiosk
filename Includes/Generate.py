import os

def generate_transaction_code():
    file_path = "transaction_code.txt"
    prefix = "A"
    start_num = 1

    # If file exists, read last number
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            last_code = f.read().strip()
            if last_code and last_code.startswith(prefix):
                num = int(last_code[1:]) + 1
            else:
                num = start_num
    else:
        num = start_num

    # Generate new code
    new_code = f"{prefix}{num:03d}"  # A001, A002, etc.

    # Save new code to file
    with open(file_path, "w") as f:
        f.write(new_code)

    return new_code
