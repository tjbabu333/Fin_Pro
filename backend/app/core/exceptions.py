class EmployeeNotFoundError(Exception):
    def __init__(self, message: str = "Employee was not found"):
        self.message = message
        super().__init__(message)


class EmployeeAlreadyExistsError(Exception):
    def __init__(self, message: str = "Employee already exists"):
        self.message = message
        super().__init__(message)


class SalaryPeriodOverlapError(Exception):
    def __init__(self, message: str = "Salary period overlaps with an existing record"):
        self.message = message
        super().__init__(message)