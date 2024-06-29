import subprocess

def run_python(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")

def main():
    print("Please enter a number of script: \n")
    print("1: CSV to DB")
    print("2: Web App")
    print("3: Phototag.ai")
    choice = input("enter command: ")

    if choice == '1':
        run_python('CSVtoDB.py')
    elif choice == '2':
        run_python('web.py')
    elif choice == '3':
        run_python('phototag.py')
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
