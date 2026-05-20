FORBIDDEN = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER"]


def validate(sql):
    s = sql.upper()

    for f in FORBIDDEN:
        if f in s:
            raise Exception(f"Blocked: {f}")

    if not s.strip().startswith("SELECT"):
        raise Exception("Only SELECT allowed")

    return True