import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------- can_register ----------
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_registered_honors_at_exact_limit():
    # 24 + 4 == 28 -> not over the limit (boundary)
    assert can_register("honors", 24, 4, True) == "registered"

def test_unknown_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 4, True)

def test_zero_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)

def test_negative_course_credits():
    with pytest.raises(ValueError):
        can_register("regular", 10, -3, True)

def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_credit_limit_exceeded_probation():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"

def test_credit_limit_exceeded_regular():
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"


# ---------- waitlist_position ----------
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

def test_zero_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)

def test_negative_capacity():
    with pytest.raises(ValueError):
        waitlist_position(10, -5, 0)

def test_class_exactly_full_goes_to_waitlist():
    assert waitlist_position(40, 40, 0) == 1

def test_waitlist_position_assigned():
    assert waitlist_position(40, 40, 3) == 4

def test_waitlist_last_slot():
    assert waitlist_position(40, 40, 9) == 10

def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1


# ---------- late_fee ----------
def test_not_late():
    assert late_fee(0, 18, False) == 0

def test_early():
    assert late_fee(-2, 18, False) == 0

def test_waiver():
    assert late_fee(5, 18, True) == 0

def test_late_within_week_normal_load():
    # days<=7 True, credits>20 False, fee>2000 False
    assert late_fee(3, 18, False) == 500

def test_late_exactly_seven_days():
    assert late_fee(7, 18, False) == 500

def test_late_within_week_heavy_load():
    # credits>20 True
    assert late_fee(3, 22, False) == 750

def test_late_over_week_not_capped():
    # 500 + 3*100 = 800
    assert late_fee(10, 18, False) == 800

def test_late_over_week_heavy_load():
    # 500 + 5*100 + 250 = 1250
    assert late_fee(12, 21, False) == 1250

def test_very_late_capped():
    # 500 + 23*100 = 2800 -> capped
    assert late_fee(30, 18, False) == 2000

def test_exactly_at_cap_not_changed():
    # 500 + 15*100 = 2000 -> fee > 2000 False
    assert late_fee(22, 18, False) == 2000
