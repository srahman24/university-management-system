import re


class UniManageSystem:
    def __init__(self):
        self.students = []
        self.courses = []

    def add_student(self, student):
        pass

    def add_course(self, course):
        pass

    def enroll_student_in_course(self, student_id, course_id):
        pass

    def get_student_courses(self, student_id):
        pass

    def get_course_students(self, course_id):
        pass

    def remove_student(self, student_id):
        pass

    def remove_course(self, course_id):
        pass

    def __str__(self):
        return f"University Management System with {len(self.students)} students and {len(self.courses)} courses."

    def __repr__(self):
        return f"UniManageSystem(students={self.students}, courses={self.courses})"

    def __len__(self):
        return len(self.students) + len(self.courses)

    def __contains__(self, item):
        if isinstance(item, Student):
            return item in self.students
        elif isinstance(item, Course):
            return item in self.courses
        return False

    def __iter__(self):
        return iter(self.students + self.courses)

    def __getitem__(self, index):
        if index < len(self.students):
            return self.students[index]
        elif index < len(self.students) + len(self.courses):
            return self.courses[index - len(self.students)]
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        if isinstance(value, Student):
            if index < len(self.students):
                self.students[index] = value
            else:
                raise IndexError("Index out of range for students")
        elif isinstance(value, Course):
            if index < len(self.students) + len(self.courses):
                self.courses[index - len(self.students)] = value
            else:
                raise IndexError("Index out of range for courses")
        else:
            raise ValueError("Value must be a Student or Course instance")

        def __delitem__(self, index):
            if index < len(self.students):
                del self.students[index]
            elif index < len(self.students) + len(self.courses):
                del self.courses[index - len(self.students)]
            else:
                raise IndexError("Index out of range")

            def __contains__(self, item):
                if isinstance(item, Student):
                    return item in self.students
                elif isinstance(item, Course):
                    return item in self.courses
                return False

            def __iter__(self):
                return iter(self.students + self.courses)

            def __len__(self):
                return len(self.students) + len(self.courses)

            def __str__(self):
                return f"University Management System with {len(self.students)} students and {len(self.courses)} courses."

            def __repr__(self):
                return (
                    f"UniManageSystem(students={self.students}, courses={self.courses})"
                )

            def __getitem__(self, index):
                if index < len(self.students):
                    return self.students[index]
                elif index < len(self.students) + len(self.courses):
                    return self.courses[index - len(self.students)]
                else:
                    raise IndexError("Index out of range")

            def __setitem__(self, index, value):
                if isinstance(value, Student):
                    if index < len(self.students):
                        self.students[index] = value
                    else:
                        raise IndexError("Index out of range for students")
                elif isinstance(value, Course):
                    if index < len(self.students) + len(self.courses):
                        self.courses[index - len(self.students)] = value
                    else:
                        raise IndexError("Index out of range for courses")
                else:
                    raise ValueError("Value must be a Student or Course instance")


class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def validate_student_id(self):
        pattern = r"^[A-Z]{2}\d{4}$"
        if re.match(pattern, self.student_id):
            return True
        else:
            return False

    def __str__(self):
        return f"Student Name: {self.name}, Student ID: {self.student_id}"

    def __repr__(self):
        return f"Student('{self.name}', '{self.student_id}')"

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.student_id == other.student_id
        return False

    def __hash__(self):
        return hash(self.student_id)


class Course:
    def __init__(self, name, course_id):
        self.name = name
        self.course_id = course_id

    def validate_course_id(self):
        pattern = r"^[A-Z]{3}\d{3}$"
        if re.match(pattern, self.course_id):
            return True
        else:
            return False

    def __str__(self):
        return f"Course Name: {self.name}, Course ID: {self.course_id}"

    def __repr__(self):
        return f"Course('{self.name}', '{self.course_id}')"

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.course_id == other.course_id
        return False

    def __hash__(self):
        return hash(self.course_id)

    def __lt__(self, other):
        if isinstance(other, Course):
            return self.course_id < other.course_id
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Course):
            return self.course_id > other.course_id
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Course):
            return self.course_id <= other.course_id
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Course):
            return self.course_id >= other.course_id
        return NotImplemented
