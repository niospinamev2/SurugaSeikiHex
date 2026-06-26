import enum

class AxisAttribute(enum.IntEnum):
    x1 = 1
    y1 = 2
    z1 = 3
    tx1 = 4
    ty1 = 5
    tz1 = 6
    x2 = 7
    y2 = 8
    z2 = 9
    tx2 = 10
    ty2 = 11
    tz2 = 12

    @staticmethod
    def from_any(value) -> "AxisAttribute":
        if isinstance(value, AxisAttribute):
            return value
        try:
            return AxisAttribute(int(value))
        except (ValueError, TypeError):
            pass
        s = str(value).lower()
        for m in AxisAttribute:
            if m.name.lower() == s:
                return m
        raise ValueError(f"Invalid axis attribute: {value!r}")