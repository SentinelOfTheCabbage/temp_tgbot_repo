from hashlib import sha256
def get_hash(pwd):
    ans = ''
    def get_x(v,l):
        v2 = ord(v)//10
        v1 = ord(v)%10
        v = int(v)

        print(v+2)
        def factorial(n):
            i = 1
            res = 1
            while i <= n:
                res *= i
                i +=1
            return res

        return v**2+factorial(v+2) + (v1*v2)*2*l
    ans = pwd
    if pwd[-1].isdigit():
        ans = f'{get_x(ans[-1],len(ans))}{pwd}'
    if pwd[0].isalpha():
        ans = f'{ans}{ord(pwd[0])}'
    return sha256(ans.encode('ASCII'))


