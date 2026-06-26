import enum

from pic_upv.suruga import System, AxisComponents


# #==================================================
# # Primera prueba
# #==================================================

# class AxisAttribute(enum.IntEnum):
#     x1 = 1
#     y1 = 2
#     z1 = 3
#     tx1 = 4
#     ty1 = 5
#     tz1 = 6
#     x2 = 7
#     y2 = 8
#     z2 = 9
#     tx2 = 10
#     ty2 = 11
#     tz2 = 12
#     @staticmethod
#     def from_any(value):
#         if isinstance(value, AxisAttribute):
#             return value
#         try:
#             return AxisAttribute(int(value))
#         except:
#             pass
#         s = str(value).lower()
#         for m in AxisAttribute:
#             if m.name.lower() == s:
#                 return m
#         raise ValueError(f"Invalid axis attribute: {value}")
    

# suruga = System()

# suruga.saludo()

# x1 = AxisComponents(suruga, 1)
# x2 = AxisComponents(suruga, AxisAttribute.from_any("x1"))
# x3 = AxisComponents(suruga, AxisAttribute.x1)

# print(x1.axis_id)
# print(x2.axis_id)
# print(x3.axis_id)


#==================================================
# Segunda prueba
#==================================================

suruga = System()

suruga.saludo()

x1 = AxisComponents(suruga, 1)             # int
x2 = AxisComponents(suruga, "x1")          # str

print(x1.axis_id)    # 1
print(x1.attribute)  # AxisAttribute.x1

print(x2.axis_id)    # 1
print(x2.attribute)  # AxisAttribute.x1