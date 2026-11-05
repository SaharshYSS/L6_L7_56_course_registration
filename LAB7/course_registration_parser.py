def format_course_code(code):
    """
    Formats 'cs 301' as 'CS301'.
    Returns None if the input is not a string with exactly two words:
    a letters-only department and a digits-only course number.
    """
    if not isinstance(code, str):
        return None
    parts = code.split()
    if len(parts) != 2:
        return None
    dept, number = parts
    if not (dept.isascii() and dept.isalpha()):
        return None
    if not (number.isascii() and number.isdigit()):
        return None
    return dept.upper() + number

def total_credits(text):
    """
    Adds up comma-separated course credits.
    Returns None if the input is not a string, if any value is empty,
    not a whole number, or negative.
    """
    if not isinstance(text, str) or not text.strip():
        return None
    total = 0
    for credit in text.split(','):
        credit = credit.strip()
        if not (credit.isascii() and credit.isdigit()):
            return None
        try:
            total += int(credit)
        except ValueError:          # e.g. an extremely long number
            return None
    return total

def parse_student_record(line):
    """
    Parses 'SRN|name|status' into a dictionary.
    Returns None if the input is not a string or does not have exactly
    three non-empty fields.
    """
    if not isinstance(line, str):
        return None
    parts = [part.strip() for part in line.split('|')]
    if len(parts) != 3 or not all(parts):
        return None
    return {"srn": parts[0].upper(),
            "name": parts[1],
            "status": parts[2].lower()}

def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    result = format_course_code(value)
    if result is None:
        print("Invalid course code. Expected format: DEPT NUMBER (e.g. cs 301)")
    else:
        print("Formatted course code:", result)

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    result = total_credits(value)
    if result is None:
        print("Invalid credits. Expected whole numbers separated by commas (e.g. 4,3,4)")
    else:
        print("Total credits:", result)

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    result = parse_student_record(value)
    if result is None:
        print("Invalid student record. Expected format: SRN|name|status")
    else:
        print("Student record:", result)

if __name__ == "__main__":
    main()
