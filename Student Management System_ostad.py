# Student Management System
import json
import os
from typing import Dict, List, Optional, Union

class Person:
    def __init__(self, name: str, age: int, address: str):
        self.name = name
        self.age = age
        self.address = address
    
    def display_person_info(self) -> None:
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")

class Student(Person):
    def __init__(self, name: str, age: int, address: str, student_id: str):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades: Dict[str, str] = {}
        self.courses: List[str] = []
    
    def add_grade(self, subject: str, grade: str) -> None:
        self.grades[subject] = grade
    
    def enroll_course(self, course: str) -> None:
        if course not in self.courses:
            self.courses.append(course)
    
    def display_student_info(self) -> None:
        print("Student Information:")
        self.display_person_info()
        print(f"ID: {self.student_id}")
        print(f"Enrolled Courses: {', '.join(self.courses) if self.courses else 'None'}")
        print(f"Grades: {self.grades if self.grades else 'No grades assigned'}")
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'student_id': self.student_id,
            'grades': self.grades,
            'courses': self.courses
        }
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """Create Student object from dictionary."""
        student = cls(data['name'], data['age'], data['address'], data['student_id'])
        student.grades = data.get('grades', {})
        student.courses = data.get('courses', [])
        return student

class Course:   
    def __init__(self, course_name: str, course_code: str, instructor: str):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students: List[str] = [] 
    
    def add_student(self, student_id: str) -> None:
        if student_id not in self.students:
            self.students.append(student_id)
    
    def display_course_info(self, student_manager) -> None:
        print("Course Information:")
        print(f"Course Name: {self.course_name}")
        print(f"Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        
        if self.students:
            student_names = []
            for student_id in self.students:
                student = student_manager.find_student(student_id)
                if student:
                    student_names.append(student.name)
            print(f"Enrolled Students: {', '.join(student_names)}")
        else:
            print("Enrolled Students: None")
    
    def to_dict(self) -> Dict:
        return {
            'course_name': self.course_name,
            'course_code': self.course_code,
            'instructor': self.instructor,
            'students': self.students
        }   
    @classmethod
    def from_dict(cls, data: Dict) -> 'Course':
        course = cls(data['course_name'], data['course_code'], data['instructor'])
        course.students = data.get('students', [])
        return course

class StudentManagementSystem:    
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.courses: Dict[str, Course] = {}
        self.data_file = "student_data.json"
    
    def find_student(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id)
    
    def find_course(self, course_code: str) -> Optional[Course]:
        return self.courses.get(course_code)
    
    def add_student(self) -> None:
        try:
            print("\n--- Add New Student ---")
            name = input("Enter Name: ").strip()
            if not name:
                print("Error: Name cannot be empty.")
                return
            
            age_str = input("Enter Age: ").strip()
            try:
                age = int(age_str)
                if age <= 0:
                    print("Error: Age must be a positive number.")
                    return
            except ValueError:
                print("Error: Please enter a valid age (number).")
                return
            
            address = input("Enter Address: ").strip()
            if not address:
                print("Error: Address cannot be empty.")
                return
            
            student_id = input("Enter Student ID: ").strip()
            if not student_id:
                print("Error: Student ID cannot be empty.")
                return
            
            if student_id in self.students:
                print(f"Error: Student with ID {student_id} already exists.")
                return
            
            student = Student(name, age, address, student_id)
            self.students[student_id] = student
            print(f"Student {name} (ID: {student_id}) added successfully.")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"Error adding student: {e}")
    
    def add_course(self) -> None:
        try:
            print("\n--- Add New Course ---")
            course_name = input("Enter Course Name: ").strip()
            if not course_name:
                print("Error: Course name cannot be empty.")
                return
            
            course_code = input("Enter Course Code: ").strip()
            if not course_code:
                print("Error: Course code cannot be empty.")
                return
            
            if course_code in self.courses:
                print(f"Error: Course with code {course_code} already exists.")
                return
            
            instructor = input("Enter Instructor Name: ").strip()
            if not instructor:
                print("Error: Instructor name cannot be empty.")
                return
            
            course = Course(course_name, course_code, instructor)
            self.courses[course_code] = course
            print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"Error adding course: {e}")
    
    def enroll_student_in_course(self) -> None:
        try:
            print("\n--- Enroll Student in Course ---")
            student_id = input("Enter Student ID: ").strip()
            course_code = input("Enter Course Code: ").strip()
            
            student = self.find_student(student_id)
            course = self.find_course(course_code)
            
            if not student:
                print(f"Error: Student with ID {student_id} not found.")
                return
            
            if not course:
                print(f"Error: Course with code {course_code} not found.")
                return
            
            if course.course_name in student.courses:
                print(f"Student {student.name} is already enrolled in {course.course_name}.")
                return
            
            student.enroll_course(course.course_name)
            course.add_student(student_id)
            print(f"Student {student.name} (ID: {student_id}) enrolled in {course.course_name} (Code: {course_code}).")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"Error enrolling student: {e}")
    
    def add_grade_for_student(self) -> None:
        try:
            print("\n--- Add Grade for Student ---")
            student_id = input("Enter Student ID: ").strip()
            course_code = input("Enter Course Code: ").strip()
            grade = input("Enter Grade: ").strip()
            
            student = self.find_student(student_id)
            course = self.find_course(course_code)
            
            if not student:
                print(f"Error: Student with ID {student_id} not found.")
                return
            
            if not course:
                print(f"Error: Course with code {course_code} not found.")
                return
            
            if course.course_name not in student.courses:
                print(f"Error: Student {student.name} is not enrolled in {course.course_name}.")
                return
            
            if not grade:
                print("Error: Grade cannot be empty.")
                return
            
            student.add_grade(course.course_name, grade)
            print(f"Grade {grade} added for {student.name} in {course.course_name}.")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"Error adding grade: {e}")
    
    def display_student_details(self) -> None:
        try:
            print("\n--- Display Student Details ---")
            student_id = input("Enter Student ID: ").strip()
            
            student = self.find_student(student_id)
            if not student:
                print(f"Error: Student with ID {student_id} not found.")
                return
            
            print()
            student.display_student_info()
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"Error displaying student details: {e}")
    
    def display_course_details(self) -> None:
        """Display details of a specific course."""
        try:
            print("\n--- Display Course Details ---")
            course_code = input("Enter Course Code: ").strip()
            
            course = self.find_course(course_code)
            if not course:
                print(f"Error: Course with code {course_code} not found.")
                return
            
            print()
            course.display_course_info(self)
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"Error displaying course details: {e}")
    
    def save_data(self) -> None:
        try:
            data = {
                'students': {sid: student.to_dict() for sid, student in self.students.items()},
                'courses': {ccode: course.to_dict() for ccode, course in self.courses.items()}
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print("All student and course data saved successfully.")
            
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self) -> None:
        try:
            if not os.path.exists(self.data_file):
                print("No data file found. Starting with empty system.")
                return
            
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            students_data = data.get('students', {})
            self.students = {sid: Student.from_dict(sdata) for sid, sdata in students_data.items()}
            
            courses_data = data.get('courses', {})
            self.courses = {ccode: Course.from_dict(cdata) for ccode, cdata in courses_data.items()}
            
            print("Data loaded successfully.")
            
        except json.JSONDecodeError:
            print("Error: Invalid data file format.")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*40)
        print("   Student Management System")
        print("="*40)
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")
        print("="*40)
    
    def run(self) -> None:
        print("Welcome to Student Management System!")
        
        self.load_data()
        
        while True:
            try:
                self.display_menu()
                choice = input("Select Option: ").strip()
                
                if choice == '1':
                    self.add_student()
                elif choice == '2':
                    self.add_course()
                elif choice == '3':
                    self.enroll_student_in_course()
                elif choice == '4':
                    self.add_grade_for_student()
                elif choice == '5':
                    self.display_student_details()
                elif choice == '6':
                    self.display_course_details()
                elif choice == '7':
                    self.save_data()
                elif choice == '8':
                    self.load_data()
                elif choice == '0':
                    print("Exiting Student Management System. Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting Student Management System. Goodbye!")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

def main():
    system = StudentManagementSystem()
    system.run()

if __name__ == "__main__":
    main()