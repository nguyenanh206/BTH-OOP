# Ho tên: Nguyễn Hà Anh
# MSSV: 202418833

import math
 
 
def require_text(value, field_name):
    if not isinstance(value, str):
        raise TypeError(f"{field_name} phải là chuỗi (str), nhận được {type(value).__name__}")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} không được rỗng")
    return cleaned
 
 
def _require_number(value, field_name):
    # bool là lớp con của int trong Python nên phải loại trừ riêng
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} phải là số, nhận được {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{field_name} phải là số hữu hạn")
    return float(value)
 
 
def require_non_negative(value, field_name):
    number = _require_number(value, field_name)
    if number < 0:
        raise ValueError(f"{field_name} không được âm (nhận được {number:,.2f})")
    return number
 
 
def require_positive(value, field_name):
    number = _require_number(value, field_name)
    if number <= 0:
        raise ValueError(f"{field_name} phải dương (nhận được {number:,.2f})")
    return number
 
