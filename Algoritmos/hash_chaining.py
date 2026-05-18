class Node:
    """Nodo para lista doblemente enlazada."""
    def __init__(self, key, data=None):
        self.key  = key
        self.data = data
        self.prev = None
        self.next = None
    def __repr__(self):
        return f"Node({self.key})"


class ChainedHashTable:
    def __init__(self, m):
        # m = número de slots de la tabla
        self.m = m
        self.T = [None] * m   # cada slot apunta a la cabeza de la lista

    def _hash(self, k):
        # Función de hash: división simple
        return k % self.m

    # ------ LIST-PREPEND(T[h(x.key)], x) ------
    def insert(self, x):
        # CHAINED-HASH-INSERT(T, x)
        slot = self._hash(x.key)
        x.next = self.T[slot]
        x.prev = None
        if self.T[slot] is not None:
            self.T[slot].prev = x
        self.T[slot] = x

    # ------ LIST-SEARCH(T[h(k)], k) ------
    def search(self, k):
        # CHAINED-HASH-SEARCH(T, k)
        slot = self._hash(k)
        node = self.T[slot]
        while node is not None:
            if node.key == k:
                return node
            node = node.next
        return None

    # ------ LIST-DELETE(T[h(x.key)], x) ------
    def delete(self, x):
        # CHAINED-HASH-DELETE(T, x)
        slot = self._hash(x.key)
        if x.prev is not None:
            x.prev.next = x.next
        else:
            self.T[slot] = x.next   # x era la cabeza
        if x.next is not None:
            x.next.prev = x.prev

    def __repr__(self):
        lines = []
        for i, head in enumerate(self.T):
            chain = []
            node = head
            while node:
                chain.append(f"{node.key}")
                node = node.next
            lines.append(f"[{i}] → " + (" → ".join(chain) if chain else "NIL"))
        return "\n".join(lines)
