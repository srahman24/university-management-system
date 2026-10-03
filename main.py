import re


# *******************************************************************************************
# University Management System Class
# *******************************************************************************************


class UniManageSystem:
    # Initiate the system with empty dictionaries for students and courses
    def __init__(self):
        self.students = {}
        self.courses = {}

    # Display the main menu of the system
    def display_menu(self):
        print("\nUniversity Management System Menu:")
        print("*" * 50)
        print("\n1.  Add Student")
        print("2.  Add Course")
        print("3.  Enroll Student in Course")
        print("4.  Get Student's Courses")
        print("5.  Get Course Students")
        print("6.  Remove Student")
        print("7.  Remove Course")
        print("8.  Add/Update Grades")
        print("9.  Find Average Grade for a Course")
        print("10. Print Student Transcript")
        print("11. Print Report - Students Ranking")
        print("12. Print Report - Failed Students")
        print("0.  Exit")
        print("*" * 50)

    # Check for duplicate student or course IDs in the system
    def check_duplicate(self, id):

        student_pattern = r"^[A-Z]{2}\d{4}$"
        course_pattern = r"^[A-Z]{2}\d{3}$"

        if re.match(student_pattern, id):
            return id in self.students

        if re.match(course_pattern, id):
            return id in self.courses

    # Add a student to the system if the student ID is not a duplicate
    def add_student(self, student):

        if not self.check_duplicate(student.student_id):
            self.students[student.student_id] = {
                "name": student.name,
                "enrolled_courses": [],
                "grades": {},
            }
            return True
        else:
            return False

    # Add a course to the system if the course ID is not a duplicate
    def add_course(self, course):
        if not self.check_duplicate(course.course_id):
            self.courses[course.course_id] = {
                "name": course.name,
                "credit": course.credit,
                "capacity": course.capacity,
                "enrolled_students": [],
                "prerequisites": course.prerequisites,
                "grades": {},
            }

            return True
        else:
            return False

    # Enroll a student in a course if the student is not already enrolled and the course has available capacity
    def enroll_student_in_course(self, student_id, course_id):

        student = self.students[student_id]
        course = self.courses[course_id]
        if course_id not in student["grades"]:
            if student_id not in course["enrolled_students"]:
                if len(course["enrolled_students"]) < course["capacity"]:
                    if all(
                        prereq in student["grades"]
                        for prereq in course["prerequisites"]
                    ):
                        student["enrolled_courses"].append(course_id)
                        course["enrolled_students"].append(student_id)
                        print(
                            f"Student {student_id} enrolled in course {course_id} successfully."
                        )
                    else:
                        print(
                            f"Student {student_id} does not meet the prerequisites for course {course_id}."
                        )
                else:
                    print(
                        f"Course {course_id} is full. Cannot enroll student {student_id}."
                    )

            else:
                print(
                    f"Student {student_id} is already enrolled in course {course_id}."
                )
        else:
            print(
                f"Student {student_id} has already completed course {course_id}. Cannot enroll again."
            )

    # List all courses a student is enrolled in
    def get_student_courses(self, student_id):
        student = self.students[student_id]
        enrolled_courses = student["enrolled_courses"]
        grades = student["grades"]

        if enrolled_courses:
            print(f"\nStudent {student_id} is enrolled in the following courses:\n")
            for course_id in enrolled_courses:
                course_name = self.courses[course_id]["name"]
                print(f"- {course_id:<10}: {course_name:<30}")
        else:
            print(f"\nStudent {student_id} is not enrolled in any courses.")

        if grades:
            print(f"\nStudent {student_id} has completed the following courses:\n")
            for course_id, gpa in grades.items():
                course_name = self.courses[course_id]["name"]
                print(f"- {course_id:<10}: {course_name:<30} | GPA: {gpa:.2f}")
        else:
            print(f"\nStudent {student_id} has not completed any courses.")

    # List all students enrolled in a course
    def get_course_students(self, course_id):
        course = self.courses[course_id]
        enrolled_students = course["enrolled_students"]
        if enrolled_students:
            print(f"\nStudents enrolled in course {course_id} ({course['name']}):\n")
            for student_id in enrolled_students:
                student_name = self.students[student_id]["name"]
                print(f"- {student_id:<10}: {student_name:<30}")
        else:
            print(f"No students enrolled in course {course_id}.")

    # Remove student from the system
    def remove_student(self, student_id):
        for course in self.courses.values():
            if student_id in course.get("enrolled_students", []):
                print(
                    f"Cannot remove student {student_id} as they are enrolled in courses."
                )
                break
        else:
            self.students.pop(student_id)
            print(f"Student {student_id} removed successfully.")

    # Remove course from the system
    def remove_course(self, course_id):
        enrolled_students = self.courses[course_id].get("enrolled_students", [])
        if enrolled_students:
            print(
                f"Cannot remove course {course_id} as there are students enrolled in it."
            )
        else:
            self.courses.pop(course_id)
            print(f"Course {course_id} removed successfully.")

    # Add/Update grades for a student in a course
    def add_update_grades(self, student_id, course_id, grade):

        # calculate GPA based on the grade
        if 80 <= grade <= 100:
            GPA = 4.0
        elif 70 <= grade < 80:
            GPA = 3.5
        elif 60 <= grade < 70:
            GPA = 3.0
        elif 50 <= grade < 60:
            GPA = 2.0
        else:
            GPA = 0.0

        self.courses[course_id]["grades"][student_id] = grade
        self.students[student_id]["grades"][course_id] = GPA

        self.students[student_id]["enrolled_courses"].remove(course_id)
        self.courses[course_id]["enrolled_students"].remove(student_id)

    # Calculate CGPA for a student based on their grades and course credits
    def calculate_cgpa(self, student_id):
        student = self.students[student_id]
        total_credits = 0
        total_grade_points = 0

        for course_id, gpa in student["grades"].items():
            course_credit = self.courses[course_id]["credit"]
            total_credits += course_credit
            total_grade_points += gpa * course_credit

        if total_credits > 0:
            cgpa = total_grade_points / total_credits
            return round(cgpa, 2)
        else:
            return 0.0

    # Print Student Transcripts
    def print_student_transcript(self, student_id):

        student = self.students[student_id]
        print("\n" + "*" * 60 + "\n")
        print(" " * 25 + "TRANSCRIPT" + " " * 25)
        print("*" * 60 + "\n\n")
        print(f"Student ID: {student_id}\nStudent Name: {student['name']}\n\n")
        print(f"{'Course ID':<10} {'Course Name':<30} {'GPA':<10}")
        print("-" * 60)
        for course_id, grade in student["grades"].items():
            course_name = self.courses[course_id]["name"]
            print(f"{course_id:<10} {course_name:<30} {grade:>10}")

        for course_id in student["enrolled_courses"]:
            print(
                f"{course_id:<10} {self.courses[course_id]['name']:<30} {'Enrolled':<10}"
            )

        print("-" * 60)
        print(f"\n Overall GPA:{self.calculate_cgpa(student_id)}")

    # print report of students ranking based on their CGPA
    def print_report_ranking(self):
        print("*" * 50 + "\n")
        print(" " * 20 + "STUDENTS RANKING" + " " * 20 + "\n")
        print("*" * 50 + "\n\n")

        student_ranking = {}

        for index, student_id in enumerate(self.students, start=1):
            cgpa = float(self.calculate_cgpa(student_id))
            student_ranking[student_id] = {
                "name": self.students[student_id]["name"],
                "cgpa": cgpa,
            }

        student_sorted = sorted(
            student_ranking.items(), key=lambda item: item[1]["cgpa"], reverse=True
        )

        for rank, (student_id, student_info) in enumerate(student_sorted, start=1):
            print(
                f"{rank}. {student_id} - {student_info['name']} - CGPA: {student_info['cgpa']}"
            )

    # Print list of failed students
    def print_report_failed_students(self):
        print("*" * 55 + "\n")
        print(" " * 20 + "FAILED STUDENTS" + " " * 20 + "\n")
        print("*" * 55 + "\n\n")

        for course_id in self.courses:
            course_grades = self.courses[course_id]["grades"]
            for student in course_grades:
                if course_grades[student] < 50:
                    print(f"{student} - {self.students[student]['name']}")
                    print(
                        f"         {self.courses[course_id]['name']} : {course_grades[student]}"
                    )


# *******************************************************************************************
# Student Class
# *******************************************************************************************


class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def validate_student_id(self, student_id):
        pattern = r"^[A-Z]{2}\d{4}$"
        return bool(re.match(pattern, student_id))


# *******************************************************************************************
# Course Class
# *******************************************************************************************


class Course:
    def __init__(self, name, course_id, credit, capacity, prerequisites):
        self.name = name
        self.course_id = course_id
        self.credit = credit
        self.capacity = capacity
        self.prerequisites = prerequisites

    def validate_course_id(self, course_id):
        pattern = r"^[A-Z]{2}\d{3}$"
        return bool(re.match(pattern, course_id))


#########################  BODY OF THE MAIN PROGRAM.  #################################

system = UniManageSystem()

while True:
    system.display_menu()

    try:
        choice = int(input("\nEnter your choice (0-12): "))
    except ValueError:
        print(" Please enter a number between 0-12, no characters please!")
        continue
    if choice == 0:
        print("Exiting the program.")
        break

    # Add student - name,student ID, enrolled course,completed course
    elif choice == 1:
        while True:
            name = input("\nEnter student name: ")
            student_id = input("Enter student ID (e.g., AB1234): ")
            student = Student(name, student_id)

            if student.validate_student_id(student_id):
                if system.add_student(student):
                    print(f"\nStudent {name} added successfully.")
                else:
                    print(f"\nStudent with ID {student_id} already exists.")
            else:
                print("\nInvalid student ID format. Please try again.")

            print("\nDo you want to add another student? (y/n): ")
            add_another = input().strip().lower()
            if add_another != "y":
                break

    # Add course - course ID, name, credit,capacity, enrolled students, prerequisites
    elif choice == 2:
        while True:
            name = input("Enter course name: ")
            course_id = input("Enter course ID (e.g., AB123): ")
            credit = int(input("Enter course credit: "))
            capacity = int(input("Enter course capacity: "))
            prerequisites_input = input(
                "Enter prerequisites (comma-separated course IDs) or leave blank if none: "
            )

            valid_prerequisites = True

            if prerequisites_input != "":
                prerequisites = [
                    prereq.strip() for prereq in prerequisites_input.split(",")
                ]

                for prereq in prerequisites:
                    if not system.courses[prereq]:
                        print(f"Prerequisite course {prereq} does not exist.")
                        valid_prerequisites = False
                        break
                    if not re.match(r"^[A-Z]{2}\d{3}$", prereq):
                        print(
                            f"Invalid prerequisite course ID format: {prereq}. Please use the format AB123."
                        )
                        valid_prerequisites = False
                        break
            else:
                prerequisites = []

            if valid_prerequisites or prerequisites_input == "":
                course = Course(name, course_id, credit, capacity, prerequisites)
                if course.validate_course_id(course_id):
                    if system.add_course(course):
                        print(f"Course {name} added successfully.")
                    else:
                        print(f"Course with ID {course_id} already exists.")
                else:
                    print("Invalid course ID format. Please try again.")
            else:
                print(
                    "Invalid prerequisites. Please ensure all prerequisites exist and are in the correct format."
                )
            print("\nDo you want to add another course? (y/n): ")
            add_another = input().strip().lower()
            if add_another != "y":
                break

    # Enrol student in course, checks for prerequisites, capacity, and if student is already enrolled
    elif choice == 3:
        student_id = input("Enter student ID to enroll: ")

        while True:
            course_id = input("Enter course ID to enroll in: ")

            if student.validate_student_id(student_id) and course.validate_course_id(
                course_id
            ):
                if student_id in system.students and course_id in system.courses:
                    system.enroll_student_in_course(student_id, course_id)
                else:
                    print("Student ID or Course ID does not exist in the system.")

            else:
                print("Invalid student ID or course ID format. Please try again.")

            print("\nDo you want to enroll the student to another course? (y/n): ")
            enroll_another = input().strip().lower()
            if enroll_another != "y":
                break

    # Get all courses a student is enrolled in
    elif choice == 4:
        student_id = input("Enter student ID to get courses: ")
        if student.validate_student_id(student_id):
            if student_id in system.students:
                system.get_student_courses(student_id)
            else:
                print(f"Student with ID {student_id} does not exist.")
        else:
            print("Invalid student ID format. Please try again.")

    # List all students enrolled in a course
    elif choice == 5:
        course_id = input("Enter course ID to get list of enrolled students: ")
        if course.validate_course_id(course_id):
            if course_id in system.courses:
                system.get_course_students(course_id)
            else:
                print(f"Course with ID {course_id} does not exist.")
        else:
            print("Invalid course ID format. Please try again.")

    # Remove student from the system
    elif choice == 6:
        student_id = input("Enter student ID to remove: ")
        if student.validate_student_id(student_id):
            if student_id in system.students:
                system.remove_student(student_id)
            else:
                print(f"Student with ID {student_id} does not exist.")
        else:
            print("Invalid student ID format. Please try again.")

    # Remove course from the system
    elif choice == 7:
        course_id = input("Enter course ID to remove: ")
        if course.validate_course_id(course_id):
            if course_id in system.courses:
                system.remove_course(course_id)
            else:
                print(f"Course with ID {course_id} does not exist.")
        else:
            print("Invalid course ID format. Please try again.")

    # Add/Update grades for a student in a course
    elif choice == 8:
        course_id = input("Enter course ID for the grade: ")
        while True:
            student_id = input("Enter student ID to add/update grades: ")

            grade = float(input("Enter Marks for the course (within 0-100): "))

            if student.validate_student_id(student_id) and course.validate_course_id(
                course_id
            ):
                if student_id in system.students and course_id in system.courses:
                    if course_id in system.students[student_id]["enrolled_courses"]:
                        if grade >= 0 and grade <= 100:
                            system.add_update_grades(student_id, course_id, grade)
                            print(
                                f"Grade added/updated for student {student_id} in course {course_id}."
                            )
                        else:
                            print(
                                "Invalid grade. Please enter a grade between 0 and 100."
                            )
                    else:
                        print(
                            f"Student {student_id} is not enrolled in course {course_id}. Cannot add/update grade."
                        )
                else:
                    print("Student ID or Course ID does not exist in the system.")
            else:
                print("Invalid student ID or course ID format. Please try again.")

            print("\nDo you want to add/update grades for another student? (y/n): ")
            add_another = input().strip().lower()
            if add_another != "y":
                break

    # Find Average Grade for a Course
    elif choice == 9:
        course_id = input("Enter course ID to find average grade: ")
        if course.validate_course_id(course_id):
            if course_id in system.courses:
                grades = system.courses[course_id]["grades"].values()
                if grades:
                    average_grade = sum(grades) / len(grades)
                    print(
                        f"Course Code: {course_id}\n\nCourse Name: {system.courses[course_id]['name']}"
                    )
                    print(
                        f"No.. of Students: {len(grades)}\nAverage Grade: {average_grade:.2f}"
                    )
                else:
                    print(f"No grades available for course {course_id}.")
            else:
                print(f"Course with ID {course_id} does not exist.")
        else:
            print("Invalid course ID format. Please try again.")

    # Print Student Transcript
    elif choice == 10:
        student_id = input("Enter student ID to print transcript: ")
        if student.validate_student_id(student_id):
            if student_id in system.students:
                system.print_student_transcript(student_id)
            else:
                print(f"Student with ID {student_id} does not exist.")
        else:
            print("Invalid student ID format. Please try again.")

    # Print Students Rankings based on CGPA
    elif choice == 11:
        system.print_report_ranking()

    # Print list of failed students
    elif choice == 12:
        system.print_report_failed_students()

    else:
        print("Invalid choice. Please try again.")
