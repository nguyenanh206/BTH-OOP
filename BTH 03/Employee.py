# Họ tên: Nguyễn Hà Anh 
# MSSV: 202418833

from Valid import require_non_negative, require_positive, require_text
 
 
class Employee:
    
    # Giá trị mặc định theo đề bài
    DEFAULT_ID = "UNKNOWN"
    DEFAULT_FULL_NAME = "Unnamed employee"
    DEFAULT_BASE_SALARY = 0.0
 
    def __init__(self, employee_id=DEFAULT_ID, full_name=DEFAULT_FULL_NAME,
                 base_salary=DEFAULT_BASE_SALARY):
        
        self._id = require_text(employee_id, "Mã nhân sự")
        self._full_name = require_text(full_name, "Họ tên")
        self._base_salary = require_non_negative(base_salary, "Lương cơ bản") 
        self._ready = True# Đánh dấu đối tượng đã dựng xong
    @property
    def id(self):
        return self._id
 
    @property
    def full_name(self):
        return self._full_name
 
    @property
    def base_salary(self):
        return self._base_salary
 
    def increase_salary(self, value, by_percentage=False):
     
        if not isinstance(by_percentage, bool):
            raise TypeError("by_percentage phải là bool (True/False)")
        value = require_positive(value, "Giá trị tăng lương")
        if by_percentage:
            self._base_salary += self._base_salary * value / 100.0
        else:
            self._base_salary += value
 
    def calculate_monthly_cost(self):
        return self._base_salary
 
    def display_info(self):
        print(f"[Employee] Mã: {self._id} | Họ tên: {self._full_name} | "
              f"Lương cơ bản: {self._base_salary:,.0f} | "
              f"Chi phí tháng: {self.calculate_monthly_cost():,.0f}")
 
    def __del__(self):
        if getattr(self, "_ready", False):
            print(f"[Employee] Hủy đối tượng {self._id}")