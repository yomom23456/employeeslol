"""
Student information for this assignment:

Replace <Anika Koppula> with your name.
On my/our honor, <Anika Koppula> and <Saisrikar Kichili>, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: ark3398
UT EID 2: srk2749
"""

from abc import ABC, abstractmethod
import random

DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."


# TODO: implement this class. You may delete this comment when you are done.
class Employee(ABC):
    """
    Abstract base class representing a generic employee in the system.
    """

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.is_employed = True
        self.__name = name
        self.__manager = manager
        self.performance = INITIAL_PERFORMANCE
        self.happiness = INITIAL_HAPPINESS
        self.salary = salary

    @property
    def salary(self):
        return self.__salary
    @salary.setter
    def salary(self,value):
        if value < 0:
            raise ValueError(SALARY_ERROR_MESSAGE)
        self.__salary = value
    @property
    def manager(self):
        return self.__manager
    @property
    def name(self):
        return self.__name  
    @property
    def happiness(self):
        return self.__happiness  
    @happiness.setter
    def happiness(self, value):
        self.__happiness = max(PERCENTAGE_MIN, min(PERCENTAGE_MAX, value))  
    @property
    def performance(self):
        return self.__performance 
    @performance.setter
    def performance(self,value):
        self.__performance = max(PERCENTAGE_MIN, min(PERCENTAGE_MAX, value))
    @abstractmethod
    def work(self):
        pass   
    def interact(self, x):
        if x.name not in self.relationships:
            self.relationships[x.name] = 0
        y = self.relationships[x.name]

        if y >= RELATIONSHIP_THRESHOLD:
            self.happiness += 1
        elif self.happiness >= HAPPINESS_THRESHOLD and x.happiness >= HAPPINESS_THRESHOLD:
            self.relationships[x.name] += 1
        else:
            self.relationships[x.name] -= 1
            self.happiness -= 1
    def daily_expense(self):
        self.savings -= DAILY_EXPENSE
        self.happiness -= 1
    def __str__(self):
        return (f"{self.name}\n\tSalary: ${self.salary}\n\tSavings: ${self.savings}\n\t"
                f"Happiness: {self.happiness}%\n\tPerformance: {self.performance}%")

# TODO: implement this class. You may delete this comment when you are done.
class Manager(Employee):
    def work(self):
        manager_performance = random.randint(-5, 5)
        self.performance += manager_performance
        if manager_performance <= 0:
            self.happiness -= 1
            for person in self.relationships:
                self.relationships[person] -= 1
        else:
            self.happiness += 1    

# TODO: implement this class. You may delete this comment when you are done.
class TemporaryEmployee(Employee):
    def work(self):
        manager_performance = random.randint(-15,15)
        self.performance += manager_performance
        if manager_performance <= 0:
            self.happiness -= 2
        else:
            self.happiness += 1

    def interact(self, other):
        super().interact(other)
        if isinstance(other, Manager):
           if other.happiness > HAPPINESS_THRESHOLD and self.performance >= TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
           elif other.happiness <= HAPPINESS_THRESHOLD:
                self.salary //= 2
                self.happiness -= 5
                if self.salary == 0:
                    self.is_employed = False

# TODO: implement this class. You may delete this comment when you are done.
class PermanentEmployee(Employee):
    def work(self):
        manager_performance = random.randint(-10,10)
        self.performance += manager_performance
        if manager_performance >= 0:
            self.happiness += 1

    def interact(self, other):
        super().interact(other)
        if isinstance(other, Manager):
            if other.happiness > HAPPINESS_THRESHOLD and self.performance > PERM_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness -= 1
                
