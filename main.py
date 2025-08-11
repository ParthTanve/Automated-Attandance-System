# main.py
from register import register_new_face
from attendance import run_attendance

def main():
    print("\n=== Automated Attendance System ===")
    print("1. Register a new face")
    print("2. Mark attendance")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ").strip()

    if choice == '1':
        register_new_face()
    elif choice == '2':
        run_attendance()
    elif choice == '3':
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
