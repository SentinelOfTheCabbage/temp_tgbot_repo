t = 0
a = [31,1]
b = [53,1]
c = [71,1]
while True:
    M = [a[0]*a[1], b[0]*b[1],c[0]*c[1]]
    dt = min(M)
    ind = M.index(dt)
    if t >= a[0]*(a[1]+1):
        a.append(a[0]*(a[1]+1))
        a[1] += 1

    if t >= b[0]*(b[1]+1):
        b.append(b[0]*(b[1]+1))
        b[1] += 1

    if t >= c[0]*(c[1]+1):
        c.append(c[0]*(c[1]+1))
        c[1] += 1

    if max(len(a),len(b),len(c)) > 12:
        print(t)
        break

    t = max(dt,t)+[10,20,40][ind]
    if ind == 0:
        a = a[:2] + a[3:]
    if ind == 1:
        b = b[:2] + b[3:]
    if ind == 2:
        c = c[:2] + c[3:]