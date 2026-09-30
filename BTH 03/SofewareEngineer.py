# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

 
from Employee import Employee
from Valid import require_non_negative, require_text
 
 
class SoftwareEngineer(Employee):
 
    def __init__(self, employee_id, full_name, *args):
        if len(args) == 1:
            base_salary, primary_language, allowance = 0.0, args[0], 0.0
        elif len(args) == 3:
            base_salary, primary_language, allowance = args
        else:
            raise TypeError(
                "SoftwareEngineer nhận (id, full_name, primary_language) hoặc "
                "(id, full_name, base_salary, primary_language, technical_allowance)")
        super().__init__(employee_id, full_name, base_salary)
        language = require_text(primary_language, "Ngôn ngữ lập trình chính")
        allowance = require_non_negative(allowance, "Phụ cấp kỹ thuật")
        self._primary_language = language
        self._technical_allowance = allowance
 
    @property
    def primary_language(self):
        return self._primary_language
 
    @property
    def technical_allowance(self):
        return self._technical_allowance
 
    def calculate_monthly_cost(self):
        return self.base_salary + self._technical_allowance
 
    def display_info(self):
        print(f"[SoftwareEngineer] Mã: {self.id} | Họ tên: {self.full_name} | "
              f"Ngôn ngữ: {self._primary_language} | "
              f"Lương cơ bản: {self.base_salary:,.0f} | "
              f"Phụ cấp: {self._technical_allowance:,.0f} | "
              f"Chi phí tháng: {self.calculate_monthly_cost():,.0f}")
 
    def __del__(self):
        if hasattr(self, "_technical_allowance"):
            print(f"[SoftwareEngineer] Hủy đối tượng {self.id}")
        super().__del__()