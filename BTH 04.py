# Họ Tên: Nguyễn Hà Anh
# MSSV: 202418833

from abc import ABC, abstractmethod

class Employee(ABC):
    # Nạp chồng constructor mô phỏng bằng tham số mặc định
    def __init__(self, employeeId, fullName, department="Unassigned"):
        self._employeeId = str(employeeId).strip()
        self._fullName = str(fullName).strip()
        self._department = str(department).strip()
        self._monthlyBonus = 0.0

        if not self._employeeId:
            raise ValueError("Mã nhân sự không được rỗng.")
        if not self._fullName:
            raise ValueError("Họ tên không được rỗng.")
        if not self._department:
            raise ValueError("Phòng ban không được rỗng.")

    @property
    def id(self):
        return self._employeeId

    @property
    def department(self):
        return self._department

    # Nạp chồng phương thức addBonus mô phỏng bằng *args
    def addBonus(self, *args):
        amount = 0.0
        reason = ""
        
        if len(args) == 1:
            # addBonus(amount)
            amount = args[0]
        elif len(args) == 2:
            # addBonus(amount, reason)
            amount, reason = args[0], str(args[1]).strip()
            if not reason: raise ValueError("Lý do không được rỗng.")
        elif len(args) == 3:
            # addBonus(rate, referenceAmount, reason)
            rate, refAmount, reason = args[0], args[1], str(args[2]).strip()
            if not (0 < rate <= 0.5):
                raise ValueError("Tỷ lệ thưởng phải > 0 và <= 0.5")
            if refAmount <= 0:
                raise ValueError("Giá trị tham chiếu phải > 0")
            if not reason: raise ValueError("Lý do không được rỗng.")
            amount = rate * refAmount
        else:
            raise TypeError("Sai số lượng tham số cho hàm add_bonus")

        if amount <= 0:
            raise ValueError("Số tiền thưởng phải > 0")
        
        self._monthlyBonus += amount

    def reset_bonus(self):
        self._monthlyBonus = 0.0

    @abstractmethod
    def calculateGrossPay(self):
        pass

    @abstractmethod
    def getEmployeeType(self):
        pass

    def displayPayrollInfo(self):
        gross_pay = self.calculateGrossPay()
        print(f"[{self.getEmployeeType()}] ID: {self._employeeId} | Tên: {self._fullName} | Phòng: {self._department} | Thưởng: {self._monthlyBonus:,.0f} | Thu nhập: {gross_pay:,.0f}")


class SalariedEmployee(Employee):
    def __init__(self, employeeId, fullName, department="Unassigned", monthlySalary=0.0, responsibilityAllowance=0.0):
        super().__init__(employeeId, fullName, department)
        self._monthlySalary = float(monthlySalary)
        self._responsibilityAllowance = float(responsibilityAllowance)

        if self._monthlySalary < 0 or self._responsibilityAllowance < 0:
            raise ValueError("Lương và phụ cấp không được âm.")

    def calculateGrossPay(self):
        return self._monthlySalary + self._responsibilityAllowance + self._monthlyBonus

    def getEmployeeType(self):
        return "Salaried"


class HourlyEmployee(Employee):
    def __init__(self, employeeId, fullName, department="Unassigned", hourlyRate=0.0, workedHours=0.0):
        super().__init__(employeeId, fullName, department)
        self._hourlyRate = float(hourlyRate)
        self._workedHours = float(workedHours)

        if self._hourlyRate < 0:
            raise ValueError("Đơn giá giờ không được âm.")
        if not (0 <= self._workedHours <= 250):
            raise ValueError("Số giờ làm phải từ 0 đến 250.")

    def calculateGrossPay(self):
        if self._workedHours <= 160:
            basePay = self._workedHours * self._hourlyRate
        else:
            basePay = 160 * self._hourlyRate + (self._workedHours - 160) * self._hourlyRate * 1.5
        return basePay + self._monthlyBonus

    def getEmployeeType(self):
        return "Hourly"


class SalesEmployee(Employee):
    def __init__(self, employeeId, fullName, department="Unassigned", baseSalary=0.0, salesRevenue=0.0, commissionRate=0.0):
        super().__init__(employeeId, fullName, department)
        self._baseSalary = float(baseSalary)
        self._salesRevenue = float(salesRevenue)
        self._commissionRate = float(commissionRate)

        if self._baseSalary < 0 or self._salesRevenue < 0:
            raise ValueError("Lương cơ bản và doanh số không được âm.")
        if not (0 <= self._commissionRate <= 0.3):
            raise ValueError("Tỷ lệ hoa hồng phải từ 0 đến 0.3.")

    def updateSales(self, additionalRevenue):
        if additionalRevenue < 0: raise ValueError("Doanh số thêm không được âm.")
        self._salesRevenue += additionalRevenue

    def calculateGrossPay(self):
        return self._baseSalary + (self._salesRevenue * self._commissionRate) + self._monthlyBonus

    def getEmployeeType(self):
        return "Sales"


class Payroll:
    def __init__(self, period):
        self._period = period
        self._employees = []

    def addEmployee(self, employee):
        if self.findEmployee(employee.id):
            print(f"Lỗi: Nhân sự mã {employee.id} đã tồn tại trong bảng lương.")
            return False
        self._employees.append(employee)
        return True

    def findEmployee(self, employeeId):
        for emp in self._employees:
            if emp.id == employeeId:
                return emp
        return None

    def calculateTotalPayroll(self):
        return sum(emp.calculateGrossPay() for emp in self._employees)

    def calculatePayrollByDepartment(self, department):
        return sum(emp.calculateGrossPay() for emp in self._employees if emp.department == department)

    def findHighestPaidEmployee(self):
        if not self._employees: return None
        return max(self._employees, key=lambda emp: emp.calculateGrossPay())

    def displayPayroll(self):
        print(f"\n--- BẢNG LƯƠNG KỲ: {self._period} ---")
        if not self._employees:
            print("Danh sách trống.")
            return
        for emp in self._employees:
            emp.displayPayrollInfo()
        print("-" * 40)


# ==========================================
# C: KIỂM THỬ VÀ BIÊN (TEST SCRIPT)
# ==========================================
def run_tests():
    payroll = Payroll("2026-09")

    print("\n[1] TEST THEO DỮ LIỆU ĐỀ BÀI")
    e1 = SalariedEmployee("E001", "Nguyễn Minh An", "Đào tạo", 15000000, 2000000)
    e1.addBonus(1000000) # Phiên bản 1: Cố định
    payroll.addEmployee(e1)

    e2 = HourlyEmployee("E002", "Trần Thu Bình", "Hỗ trợ", 100000, 150)
    e2.addBonus(500000, "Thưởng chuyên cần") # Phiên bản 2: Cố định + lý do
    payroll.addEmployee(e2)

    e3 = HourlyEmployee("E003", "Lê Hoàng Chi", "Hỗ trợ", 100000, 170)
    payroll.addEmployee(e3)

    e4 = SalesEmployee("E004", "Phạm Quốc Dũng", "Kinh doanh", 8000000, 200000000, 0.05)
    e4.addBonus(0.02, 50000000, "Thưởng đạt mốc quý") # Phiên bản 3: Tỷ lệ
    payroll.addEmployee(e4)

    payroll.displayPayroll()

    print(f"Tổng bảng lương: {payroll.calculateTotalPayroll():,.0f} (Kỳ vọng: 70,000,000)")
    print(f"Tổng phòng Hỗ trợ: {payroll.calculatePayrollByDepartment('Hỗ trợ'):,.0f} (Kỳ vọng: 33,000,000)")
    
    highestEmployee = payroll.findHighestPaidEmployee()
    print(f"Thu nhập cao nhất: {highestEmployee.id} - {highestEmployee.calculateGrossPay():,.0f}")

    print("\n[2] KIỂM THỬ BIÊN VÀ LỖI (10 TÌNH HUỐNG)")
    def testError(testName, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            print(f"  [X] Thất bại ở {testName}: Lỗi không được ném ra!")
        except Exception as e:
            print(f"  [v] Pass {testName} - Ném lỗi chuẩn xác: {e}")

    # 1. Thêm nhân sự trùng mã
    print(" 1. Thêm trùng mã:")
    payroll.addEmployee(e1) 
    
    # 2. Mã rỗng
    testError("2. Tạo NV mã rỗng", SalariedEmployee, "", "Test", "IT", 100)
    
    # 3. Lương âm
    testError("3. Lương âm", SalariedEmployee, "E005", "Test", "IT", -10)
    
    # 4. Thưởng âm
    testError("4. Thưởng âm", e1.addBonus, -5000)
    
    # 5. Giờ làm < 0
    testError("5. Giờ làm âm", HourlyEmployee, "E006", "Test", "IT", 100, -5)
    
    # 6. Giờ làm > 250
    testError("6. Giờ làm vượt 250", HourlyEmployee, "E007", "Test", "IT", 100, 251)
    
    # 7. Tỷ lệ hoa hồng < 0
    testError("7. Hoa hồng âm", SalesEmployee, "E008", "Test", "IT", 100, 100, -0.1)
    
    # 8. Tỷ lệ hoa hồng > 0.3
    testError("8. Hoa hồng > 0.3", SalesEmployee, "E009", "Test", "IT", 100, 100, 0.4)
    
    # 9. Tỷ lệ thưởng addBonus > 0.5
    testError("9. Thưởng tỷ lệ > 0.5", e4.addBonus, 0.6, 1000, "Lý do")
    
    # 10. addBonus thiếu lý do (chuỗi rỗng)
    testError("10. Thưởng rỗng lý do", e4.addBonus, 1000, "")

if __name__ == "__main__":
    run_tests()