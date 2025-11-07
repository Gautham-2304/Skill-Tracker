import os
import csv
from datetime import date
import matplotlib.pyplot as plt
from fpdf import FPDF
from shutil import copyfile
from datetime import datetime

def initialize_csv():
    filename = "skills.csv"
    
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["skill_name", "current_level", "target_level", "last_updated"])
        print("skills.csv created with headers ✅")
    else:
        print("skills.csv already exists ✅")


def show_menu():
    print("\n----Smart Skill Tracker----")
    print("""Choose an option from the menu:
          1. Add Skill
          2. Update Skill
          3. Delete Skill
          4. Track/View Skills
          5. Filter skills
          6. Visual chart of skills
          7. Export data (PDF/CSV)
          8. Sort Skills
          9. Exit""")
    
def add_skill():
    skill_name = input("Enter skill name: ").strip()
    
    while True:
        try:
            current_level = int(input("Enter current level (0-100): "))
            if 0 <= current_level <= 100:
                break
            else:
                print("Level must be between 0 and 100!")
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            target_level = int(input("Enter target level (0-100): "))
            if 0 <= target_level <= 100:
                break
            else:
                print("Level must be between 0 and 100!")
        except ValueError:
            print("Please enter a valid number.")

    last_updated = date.today().strftime("%Y-%m-%d")

    # Append to CSV
    with open("skills.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([skill_name, current_level, target_level, last_updated])
    
    print(f"Skill '{skill_name}' added successfully ✅")

def view_skills():
    try:
        with open("skills.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            skills = list(reader)

            if len(skills) <= 1:
                print("No skills found. Add some first!")
                return

            # Print headers
            headers = skills[0]
            print(f"\n{headers[0]:<20} {headers[1]:<15} {headers[2]:<15} {headers[3]:<12}")
            print("-" * 65)

            # Print each skill
            for row in skills[1:]:
                print(f"{row[0]:<20} {row[1]:<15} {row[2]:<15} {row[3]:<12}")

    except FileNotFoundError:
        print("skills.csv not found. Please add a skill first!")

def filter_skills():
    try:
        with open("skills.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            skills = list(reader)

            if len(skills) <= 1:
                print("No skills found. Add some first!")
                return

            # Ask the user how they want to filter
            print("\nFilter options:")
            print("1. Show skills above a certain current level")
            print("2. Show skills below target level")
            print("3. Search skill by name")
            choice = input("Enter choice (1-3): ").strip()

            if choice == '1':
                level = int(input("Enter minimum current level: "))
                filtered = [row for row in skills[1:] if int(row[1]) >= level]
            elif choice == '2':
                filtered = [row for row in skills[1:] if int(row[1]) < int(row[2])]
            elif choice == '3':
                name = input("Enter skill name to search: ").strip().lower()
                filtered = [row for row in skills[1:] if name in row[0].lower()]
            else:
                print("Invalid choice!")
                return

            if not filtered:
                print("No skills matched the filter.")
                return

            # Print filtered skills
            headers = skills[0]
            print(f"\n{headers[0]:<20} {headers[1]:<15} {headers[2]:<15} {headers[3]:<12}")
            print("-" * 65)
            for row in filtered:
                print(f"{row[0]:<20} {row[1]:<15} {row[2]:<15} {row[3]:<12}")

    except FileNotFoundError:
        print("skills.csv not found. Please add a skill first!")

def visual_chart():
    try:
        with open("skills.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            skills = list(reader)

            if len(skills) <= 1:
                print("No skills found. Add some first!")
                return

            skill_names = [row[0] for row in skills[1:]]
            current_levels = [int(row[1]) for row in skills[1:]]
            target_levels = [int(row[2]) for row in skills[1:]]

            x = range(len(skill_names))

            plt.figure(figsize=(10,6))
            plt.bar(x, current_levels, width=0.4, label="Current Level", color='skyblue', align='center')
            plt.bar(x, target_levels, width=0.4, label="Target Level", color='lightgreen', alpha=0.5, align='edge')

            plt.xticks(x, skill_names, rotation=30)
            plt.xlabel("Skills")
            plt.ylabel("Level")
            plt.title("Skill Progress")
            plt.legend()
            plt.tight_layout()
            plt.show()

    except FileNotFoundError:
        print("skills.csv not found. Please add a skill first!")

def export_data():
    try:
        with open("skills.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            skills = list(reader)

            if len(skills) <= 1:
                print("No skills found to export. Add some first!")
                return

            # Ask user whether CSV or PDF
            print("\nExport options:")
            print("1. CSV")
            print("2. PDF")
            choice = input("Enter choice (1-2): ").strip()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if choice == '1':
                export_filename = f"skills_export_{timestamp}.csv"
                copyfile("skills.csv", export_filename)
                print(f"CSV exported successfully as {export_filename} ✅")

            elif choice == '2':
                export_filename = f"skills_export_{timestamp}.pdf"
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "Skill Tracker Report", ln=True, align="C")
                pdf.ln(10)

                pdf.set_font("Arial", "B", 12)
                # Add table headers
                headers = skills[0]
                pdf.cell(50, 10, headers[0], 1)
                pdf.cell(40, 10, headers[1], 1)
                pdf.cell(40, 10, headers[2], 1)
                pdf.cell(40, 10, headers[3], 1)
                pdf.ln()

                pdf.set_font("Arial", "", 12)
                for row in skills[1:]:
                    pdf.cell(50, 10, row[0], 1)
                    pdf.cell(40, 10, row[1], 1)
                    pdf.cell(40, 10, row[2], 1)
                    pdf.cell(40, 10, row[3], 1)
                    pdf.ln()

                pdf.output(export_filename)
                print(f"PDF exported successfully as {export_filename} ✅")

            else:
                print("Invalid choice! Export canceled.")

    except FileNotFoundError:
        print("skills.csv not found. Please add a skill first!")

def update_skill():
    try:
        with open("skills.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            skills = list(reader)

            if len(skills) <= 1:
                print("No skills found to update. Add some first!")
                return

        skill_name = input("Enter the skill name to update: ").strip().lower()
        found = False

        for i, row in enumerate(skills[1:], start=1):
            if row[0].lower() == skill_name:
                found = True
                print(f"Current Level: {row[1]}, Target Level: {row[2]}")

                while True:
                    try:
                        new_current = int(input("Enter new current level (0-100): "))
                        if 0 <= new_current <= 100:
                            break
                        else:
                            print("Level must be between 0 and 100!")
                    except ValueError:
                        print("Please enter a valid number.")

                while True:
                    try:
                        new_target = int(input("Enter new target level (0-100): "))
                        if 0 <= new_target <= 100:
                            break
                        else:
                            print("Level must be between 0 and 100!")
                    except ValueError:
                        print("Please enter a valid number.")

                skills[i][1] = str(new_current)
                skills[i][2] = str(new_target)
                skills[i][3] = date.today().strftime("%Y-%m-%d")
                print(f"Skill '{row[0]}' updated successfully ✅")
                break

        if not found:
            print("Skill not found!")

        # Write updated data back to CSV
        with open("skills.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(skills)

    except FileNotFoundError:
        print("skills.csv not found. Please add a skill first!")


def delete_skill():
    try:
        with open("skills.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            skills = list(reader)

            if len(skills) <= 1:
                print("No skills found to delete. Add some first!")
                return

        skill_name = input("Enter the skill name to delete: ").strip().lower()
        new_skills = [skills[0]]  # Keep headers
        found = False

        for row in skills[1:]:
            if row[0].lower() == skill_name:
                found = True
                print(f"Skill '{row[0]}' deleted successfully ✅")
                continue
            new_skills.append(row)

        if not found:
            print("Skill not found!")

        # Write updated data back to CSV
        with open("skills.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(new_skills)

    except FileNotFoundError:
        print("skills.csv not found. Please add a skill first!")

def view_sorted_skills():
    try:
        with open("skills.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            skills = list(reader)

            if len(skills) <= 1:
                print("No skills found. Add some first!")
                return

            headers = skills[0]
            data = skills[1:]

            # Ask user for sort field with exit option
            while True:
                print("\nSort by:")
                print("1. Skill Name")
                print("2. Current Level")
                print("3. Target Level")
                print("E. Exit sorting")
                field_choice = input("Enter choice (1-3 or E to exit): ").strip().upper()
                if field_choice in ['1', '2', '3']:
                    field_index = int(field_choice) - 1
                    break
                elif field_choice == 'E':
                    print("Exiting sorting...")
                    return
                else:
                    print("Invalid choice! Please enter 1, 2, 3, or E.")

            # Ask user for sort order with exit option
            while True:
                order = input("Sort order? (A for Ascending / D for Descending / E to exit): ").strip().upper()
                if order in ['A', 'D']:
                    reverse = order == 'D'
                    break
                elif order == 'E':
                    print("Exiting sorting...")
                    return
                else:
                    print("Invalid input! Please enter 'A', 'D', or 'E'.")

            # Sort data
            if field_index == 0:
                data.sort(key=lambda x: x[field_index].lower(), reverse=reverse)
            else:
                data.sort(key=lambda x: int(x[field_index]), reverse=reverse)

            # Print headers
            print(f"\n{headers[0]:<20} {headers[1]:<15} {headers[2]:<15} {headers[3]:<12}")
            print("-" * 65)

            # Print sorted skills
            for row in data:
                print(f"{row[0]:<20} {row[1]:<15} {row[2]:<15} {row[3]:<12}")

    except FileNotFoundError:
        print("skills.csv not found. Please add a skill first!")
 
def main():
    initialize_csv()
    while True:
        show_menu()
        choice = input("Enter your choice (1-9): ")

        match choice:
            case '1':
                print("----Add Skill selected.----")
                add_skill()
            case '2':
                print("----Update Skill selected.----")
                update_skill()
            case '3':
                print("----Delete Skill selected.----")
                delete_skill()
            case '4':
                print("----Track/View Skills selected.----")
                view_skills()
            case '5':
                print("----Filter Skills selected.----")
                filter_skills()
            case '6':
                print("----Visual Chart of Skills selected.----")
                visual_chart()
            case '7':
                print("----Export Data (PDF/CSV) selected.----")
                export_data()
            case '8':
                print("----Sort Skills selected----")
                view_sorted_skills()
            case '9':
                print("----Exiting program...... Goodbye!!!----")
                break
            case _:
                print("Invalid Choice. Please try again.")

if __name__ == "__main__":
    main()