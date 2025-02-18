import csv
import re

class Student:
    def __init__(self, name, roll_no, subject, marks):
        if not re.match(r"^[A-Za-z ]+$", name):
            raise ValueError("Invalid name. Only letters and spaces allowed.")
        if not re.match(r"^\d{2}[A-Z]{2}\d{3}$", roll_no):  # Example: 22CS101
            raise ValueError("Invalid roll number format (e.g., 22CS101).")
        if not (0 <= marks <= 100):
            raise ValueError("Marks should be between 0 and 100.")

        self.name = name
        self.roll_no = roll_no
        self.subject = subject
        self.marks = marks
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.marks >= 90:
            return 'A'
        elif self.marks >= 75:
            return 'B'
        elif self.marks >= 60:
            return 'C'
        elif self.marks >= 50:
            return 'D'
        else:
            return 'F'

    def to_list(self):
        return [self.name, self.roll_no, self.subject, self.marks, self.grade]

class GradeManager:
    FILE_NAME = "grades.csv"

    def __init__(self):
        try:
            with open(self.FILE_NAME, "x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Roll No", "Subject", "Marks", "Grade"])
        except FileExistsError:
            pass  # File already exists

    def add_student(self, student):
        with open(self.FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(student.to_list())
        print(f"Student {student.name} added successfully.")

    def view_students(self):
        with open(self.FILE_NAME, "r") as file:
            reader = csv.reader(file)
            data = list(reader)

        if len(data) == 1:
            print("No student records found.")
        else:
            for row in data:
                print(", ".join(row))

    def search_student(self, roll_no):
        with open(self.FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[1] == roll_no:
                    print("Student Found: " + ", ".join(row))
                    return
        print("Student not found.")

    def delete_student(self, roll_no):
        with open(self.FILE_NAME, "r") as file:
            reader = csv.reader(file)
            students = list(reader)

        filtered_students = [students[0]]  # Keep header
        found = False
        for row in students[1:]:
            if row[1] == roll_no:
                found = True
            else:
                filtered_students.append(row)

        if found:
            with open(self.FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(filtered_students)
            print("Student record deleted successfully.")
        else:
            print("Student not found.")

def get_valid_input(prompt, pattern, error_message):
    while True:
        value = input(prompt)
        if re.match(pattern, value):
            return value
        print(error_message)

def get_valid_marks():
    while True:
        try:
            marks = int(input("Enter marks (0-100): "))
            if 0 <= marks <= 100:
                return marks
            else:
                print("Marks should be between 0 and 100.")
        except ValueError:
            print("Invalid marks. Please enter a number between 0 and 100.")

def main():
    manager = GradeManager()

    while True:
        print("\nStudent Grade Management System")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by Roll No")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = get_valid_input("Enter student name: ", r"^[A-Za-z ]+$", "Invalid name. Only letters and spaces allowed.")
            roll_no = get_valid_input("Enter roll number (e.g., 22CS101): ", r"^\d{2}[A-Z]{2}\d{3}$", "Invalid roll number format (e.g., 22CS101).")
            subject = input("Enter subject: ")
            marks = get_valid_marks()

            student = Student(name, roll_no, subject, marks)
            manager.add_student(student)

        elif choice == "2":
            manager.view_students()

        elif choice == "3":
            roll_no = input("Enter roll number: ")
            manager.search_student(roll_no)

        elif choice == "4":
            roll_no = input("Enter roll number: ")
            manager.delete_student(roll_no)

        elif choice == "5":
            print("Exiting... Goodbye.")
            break

        else:
            print("Invalid choice. Please try again.")
main()
