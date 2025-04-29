import os
from datetime import datetime

def show_menu():
    print("\n===== Rapid Response Hub =====")
    print("1. Report a Disaster")
    print("2. View Past Reports")
    print("3. Exit")

def report_disaster():
    disaster_types = ["Flood", "Fire", "Earthquake", "Drought"]

    print("\nSelect Disaster Type:")
    for i, disaster in enumerate(disaster_types, 1):
        print(f"{i}. {disaster}")

    choice = input("Enter your choice (1-4): ")

    if choice.isdigit() and 1 <= int(choice) <= 4:
        selected_disaster = disaster_types[int(choice) - 1]
        location = input("Enter the location of the disaster: ")
        description = input("Enter a short description: ")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = (
            f"Time: {now}\n"
            f"Disaster Type: {selected_disaster}\n"
            f"Location: {location}\n"
            f"Description: {description}\n\n"
        )

        with open("disaster_reports.txt", "a") as file:
            file.write(report)

        print("✅ Report submitted successfully!")
    else:
        print("❌ Invalid selection. Try again.")

def view_reports():
    print("\n===== Past Disaster Reports =====")
    if os.path.exists("disaster_reports.txt"):
        with open("disaster_reports.txt", "r") as file:
            print(file.read())
    else:
        print("No reports found yet.")

def main():
    while True:
        show_menu()
        option = input("Choose an option (1-3): ")

        if option == '1':
            report_disaster()
        elif option == '2':
            view_reports()
        elif option == '3':
            print("Exiting... Stay safe!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
