from pic_upv.suruga import System, AxisComponents

suruga = System()

suruga.saludo()

x1 = AxisComponents(suruga, "x1")

# Tan solo quiero confirmar que el nombre coincida con el numero del eje
print(x1.attribute)

suruga.conectar()

# # Movimiento en +x teniendo como referencia la camara
# x1.move_relative(63.5, speed=20.0) 

# Movimiento en -x teniendo como referencia la camara
x1.move_relative(-63.5, speed=20.0) 


# Quiero confirmar que la clase axis_components puede acceder a los metodos de 
# la clase AxisComponents del dll srgmc.dll
# print(x1.axis.SetMaxSpeed(20))
# print(x1.axis.SetAccelRate(100))
