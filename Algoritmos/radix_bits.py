def valor_bit(numero, bit):
    mask = 1 << bit
    if numero & mask != 0:
        return 1
    return 0 

def counting_bit_sort(lista, bit):
    counts = [0,0]
    for i in lista:
        counts[ valor_bit(i, bit) ] += 1

    indices = [0, counts[0]]

    lista_ordenada = [None] * len(lista)

    for i in lista:
        item_valor_bit = valor_bit(i, bit)
        lista_ordenada[ indices[item_valor_bit]] = i
        indices[item_valor_bit] += 1

    return lista_ordenada

def radix_bit_sort(lista):
    for i in range(64):
        lista = counting_bit_sort(lista, i)

    return lista




arr = [234, 356, 343, 864, 324, 356, 896, 123]
x = radix_bit_sort(arr)
print(x)