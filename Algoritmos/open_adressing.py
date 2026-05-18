class OpenAddressHashTable:
    _NIL     = object()   # slot vacío nunca usado
    _DELETED = object()   # slot eliminado (tombstone)

    def __init__(self, m, probe="linear", c1=1, c2=1):
        self.m     = m
        self.T     = [self._NIL] * m
        self.probe = probe   # "linear" | "quadratic" | "double"
        self.c1    = c1
        self.c2    = c2
        self.n     = 0

    def _h_aux(self, k):
        return k % self.m

    def _h2(self, k):
        # Segunda función para double hashing: h2(k) = 1 + (k mod (m-1))
        return 1 + (k % (self.m - 1))

    def _probe_seq(self, k, i):
        # Retorna el slot para la i-ésima sonda de la clave k
        if self.probe == "linear":
            # h(k, i) = (h'(k) + i) mod m
            return (self._h_aux(k) + i) % self.m
        elif self.probe == "quadratic":
            # h(k, i) = (h'(k) + c1·i + c2·i²) mod m
            return (self._h_aux(k) + self.c1*i + self.c2*i*i) % self.m
        elif self.probe == "double":
            # h(k, i) = (h1(k) + i·h2(k)) mod m
            return (self._h_aux(k) + i * self._h2(k)) % self.m
        else:
            raise ValueError(f"Método de sondeo desconocido: {self.probe}")

    def insert(self, k):
        # HASH-INSERT(T, k)
        if self.n >= self.m:
            raise OverflowError("hash table overflow")
        i = 0
        while i < self.m:          # repeat ... until i == m
            q = self._probe_seq(k, i)
            if self.T[q] is self._NIL or self.T[q] is self._DELETED:
                self.T[q] = k      # T[q] = k  →  return q
                self.n += 1
                return q
            i += 1                 # else i = i + 1
        raise OverflowError("hash table overflow")

    def search(self, k):
        # HASH-SEARCH(T, k)
        i = 0
        while i < self.m:
            q = self._probe_seq(k, i)
            if self.T[q] == k:
                return q           # return q (posición encontrada)
            if self.T[q] is self._NIL:
                return None        # until T[q] == NIL
            i += 1
        return None

    def delete(self, k):
        # Marcamos con DELETED para no romper las cadenas de sondeo
        pos = self.search(k)
        if pos is None:
            raise KeyError(k)
        self.T[pos] = self._DELETED
        self.n -= 1

    def __repr__(self):
        rows = []
        for i, v in enumerate(self.T):
            if   v is self._NIL:     rows.append(f"[{i:2d}] NIL")
            elif v is self._DELETED: rows.append(f"[{i:2d}] DELETED")
            else:                    rows.append(f"[{i:2d}] {v}")
        return "\n".join(rows)
