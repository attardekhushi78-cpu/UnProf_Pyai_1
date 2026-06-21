import tkinter as tk
from tkinter import messagebox, ttk


# BACKEND ARCHITECTURE (OOP & Inheritance)


class Member:
    """
    Parent Class: Demonstrating Basics of Inheritance.
    """
    def __init__(self, name: str, member_id: str):
        self.name = name
        self.member_id = member_id


class Student(Member):
    """
    Child Class: Inherits from Member.
    Manages student grades and core report computations.
    """
    def __init__(self, name: str, student_id: str):
        super().__init__(name, student_id)  # Inheriting attributes via super()
        self.grades = {}  # Dictionary to store subject: grade pairs

    def add_or_update_grade(self, subject: str, grade: float):
        """Adds or updates a numeric grade."""
        self.grades[subject] = grade

    def calculate_gpa(self) -> float:
        """Calculates the overall average percentage."""
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)



# FRONTEND UI ARCHITECTURE (Tkinter)


class StudentSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Report Card System")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        # In-memory database to store created Student objects
        self.student_db = {}
        
        self.create_widgets()

    def create_widgets(self):
        # --- TITLE BANNER ---
        title = tk.Label(self.root, text="🎓 Student Report Card System", font=("Arial", 16, "bold"), fg="#2c3e50")
        title.pack(pady=15)

        # --- SEPARATOR ---
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20, pady=5)

        
        # SECTION 1: ADD STUDENT DETAILS
      
        frame_student = tk.LabelFrame(self.root, text=" 1. Add Student Details ", font=("Arial", 10, "bold"), padx=10, pady=10)
        frame_student.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_student, text="Student Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_name = tk.Entry(frame_student, width=20)
        self.ent_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_student, text="Student ID:").grid(row=0, column=2, sticky="w", pady=5)
        self.ent_id = tk.Entry(frame_student, width=15)
        self.ent_id.grid(row=0, column=3, padx=10, pady=5)

        btn_add_student = tk.Button(frame_student, text="Register Student", bg="#2ecc71", fg="white", font=("Arial", 9, "bold"), command=self.ui_add_student)
        btn_add_student.grid(row=0, column=4, padx=10, pady=5)

       
        # SECTION 2: ADD OR UPDATE GRADES
      
        frame_grades = tk.LabelFrame(self.root, text=" 2. Add / Update Grades ", font=("Arial", 10, "bold"), padx=10, pady=10)
        frame_grades.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_grades, text="Select Student ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.cb_students = ttk.Combobox(frame_grades, width=13, state="readonly")
        self.cb_students.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_grades, text="Subject:").grid(row=0, column=2, sticky="w", pady=5)
        self.ent_subject = tk.Entry(frame_grades, width=15)
        self.ent_subject.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_grades, text="Grade (0-100):").grid(row=0, column=4, sticky="w", pady=5)
        self.ent_grade = tk.Entry(frame_grades, width=6)
        self.ent_grade.grid(row=0, column=5, padx=5, pady=5)

        btn_save_grade = tk.Button(frame_grades, text="Save Grade", bg="#3498db", fg="white", font=("Arial", 9, "bold"), command=self.ui_save_grade)
        btn_save_grade.grid(row=1, column=5, pady=10, sticky="e")

        
        # SECTION 3: DISPLAY REPORT CARD
        
        frame_report = tk.LabelFrame(self.root, text=" 3. View Report Card ", font=("Arial", 10, "bold"), padx=10, pady=10)
        frame_report.pack(fill="both", expand=True, padx=20, pady=10)

        # View Selector Button
        btn_view = tk.Button(frame_report, text="Generate Selected Report Card", bg="#34495e", fg="white", font=("Arial", 9, "bold"), command=self.ui_display_report)
        btn_view.pack(anchor="w", pady=5)

        # Text Area for Displaying the actual report card nicely
        self.txt_report = tk.Text(frame_report, height=12, bg="#f8f9fa", font=("Courier", 10))
        self.txt_report.pack(fill="both", expand=True, pady=5)

    
    # LOGIC PROCESSING INTERFACES
    

    def ui_add_student(self):
        name = self.ent_name.get().strip()
        student_id = self.ent_id.get().strip()

        if not name or not student_id:
            messagebox.showwarning("Missing Information", "Please enter both Student Name and ID.")
            return

        if student_id in self.student_db:
            messagebox.showerror("Duplicate ID", "A student with this ID already exists.")
            return

        # Core OOP Action: Creating a new instance object dynamically
        new_student = Student(name, student_id)
        self.student_db[student_id] = new_student

        # Refresh dropdown values
        self.cb_students['values'] = list(self.student_db.keys())
        self.cb_students.set(student_id)

        # Clear UI Input boxes
        self.ent_name.delete(0, tk.END)
        self.ent_id.delete(0, tk.END)
        messagebox.showinfo("Success", f"Registered Student: {name} ({student_id})")

    def ui_save_grade(self):
        student_id = self.cb_students.get()
        subject = self.ent_subject.get().strip()
        grade_str = self.ent_grade.get().strip()

        if not student_id:
            messagebox.showwarning("Selection Error", "Please select a Student ID from the dropdown menu.")
            return
        if not subject or not grade_str:
            messagebox.showwarning("Missing Data", "Please fill out both Subject and Grade fields.")
            return

        try:
            grade = float(grade_str)
            if not (0 <= grade <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Grade must be a valid numeric value between 0 and 100.")
            return

        # Fetch OOP object from our record dictionary and call its internal method
        student_obj = self.student_db[student_id]
        student_obj.add_or_update_grade(subject, grade)

        # Clear inputs
        self.ent_subject.delete(0, tk.END)
        self.ent_grade.delete(0, tk.END)
        messagebox.showinfo("Grade Saved", f"Saved grade for {subject} successfully.")

    def ui_display_report(self):
        student_id = self.cb_students.get()
        if not student_id:
            messagebox.showwarning("Selection Error", "Please select a Student ID first.")
            return

        student_obj = self.student_db[student_id]

        # Formatting report visual data output buffer
        report_text = "=" * 50 + "\n"
        report_text += f"            📜 OFFICIAL STUDENT REPORT CARD 📜\n"
        report_text += "=" * 50 + "\n"
        report_text += f" Student ID   : {student_obj.member_id}\n"
        report_text += f" Student Name : {student_obj.name}\n"
        report_text += "-" * 50 + "\n"
        report_text += f" {'Subject':<30} | {'Grade':<10}\n"
        report_text += "-" * 50 + "\n"

        if not student_obj.grades:
            report_text += " No grades have been entered yet.\n"
        else:
            for sub, gr in student_obj.grades.items():
                report_text += f" {sub:<30} | {gr:<10.2f}\n"

        report_text += "-" * 50 + "\n"
        report_text += f" 📊 Cumulative Percentage GPA: {student_obj.calculate_gpa():.2f}%\n"
        report_text += "=" * 50 + "\n"

        # Push formatted buffer string into Text Component
        self.txt_report.delete("1.0", tk.END)
        self.txt_report.insert(tk.END, report_text)


# Application Lifecycle Execution 
if __name__ == "__main__":
    window = tk.Tk()
    app = StudentSystemUI(window)
    window.mainloop()