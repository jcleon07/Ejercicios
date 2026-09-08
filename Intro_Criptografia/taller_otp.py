alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def cifrar(mensaje, llave):
	if len(mensaje) != len(llave):
		print('El mensaje y la llave deben tener la misma longitud.')
		exit()

	mensaje = mensaje.upper()
	llave = llave.upper()
	resultado = ''

	for i in range(len(mensaje)):
		posicion_mensaje = alfabeto.index(mensaje[i])
		posicion_llave = alfabeto.index(llave[i])
		posicion_nueva = (posicion_mensaje + posicion_llave) % 26
		resultado += alfabeto[posicion_nueva]

	return resultado


def descifrar(mensaje, llave):
	if len(mensaje) != len(llave):
		print('El mensaje y la llave deben tener la misma longitud.')
		exit()

	mensaje = mensaje.upper()
	llave = llave.upper()
	resultado = ''

	for i in range(len(mensaje)):
		posicion_mensaje = alfabeto.index(mensaje[i])
		posicion_llave = alfabeto.index(llave[i])
		posicion_nueva = (posicion_mensaje - posicion_llave) % 26
		resultado += alfabeto[posicion_nueva]

	return resultado


operacion = input('Escriba CIFRAR o DESCIFRAR: ').upper()
mensaje = input('Escriba el mensaje en mayusculas: ')
llave = input('Escriba la llave: ')

if operacion == 'CIFRAR':
	print('Mensaje cifrado:', cifrar(mensaje, llave))
elif operacion == 'DESCIFRAR' or operacion == 'DECIFRAR':
	print('Mensaje descifrado:', descifrar(mensaje, llave))
else:
	print('Operacion no valida.')