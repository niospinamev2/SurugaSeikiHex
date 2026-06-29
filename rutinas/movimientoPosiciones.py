from pic_upv.suruga import System, AxisComponents

# ======================================================
# Inicialización
# ======================================================

suruga = System()
suruga.conectar()

x1 = AxisComponents(suruga, "x1")
x2 = AxisComponents(suruga, "x2")

# ======================================================
# Posiciones del chip relativas al origen
# ======================================================

waveguides = {
    "WG1": (63.5,  63.5),
    "WG2": (127.0, 127.0),
    "WG3": (190.5, 190.5),
}

# ======================================================
# Se asume que la máquina YA está posicionada sobre WG0
# ======================================================

origin_x1 = x1.get_actual_position()
origin_x2 = x2.get_actual_position()

print("Origen de la máquina")
print(f"X1 = {origin_x1:.3f}")
print(f"X2 = {origin_x2:.3f}")

print()

# ======================================================
# Recorrer todas las waveguides
# ======================================================

for name, (rel_x1, rel_x2) in waveguides.items():

    abs_x1 = origin_x1 + rel_x1
    abs_x2 = origin_x2 + rel_x2

    print("="*40)
    print(name)

    print(f"Relativa : ({rel_x1:.3f}, {rel_x2:.3f})")
    print(f"Absoluta : ({abs_x1:.3f}, {abs_x2:.3f})")

    x1.move_absolute(abs_x1)
    x2.move_absolute(abs_x2)

    input("Presione Enter para continuar...")