import random
id_list = []

def generate_code(length=8):
    alphabet = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    pwd = ''
    for i in range (length):
        char = alphabet[random.randint(0,len(alphabet)-1)]
        pwd += char

    return pwd

# pairs = []
# pwds = []
# for id in id_list:
#     pwd = generate_code()
#     if pwd in pwds:
#         print(id)
#     else:
#         pairs.append((id,pwd))
#         pwds.append(pwd)

# queries = []
# pattern = 'INSERT INTO bonuses (bonus_code, bonus_type, bonuses_amount, client_id) VALUES '
# for user_id,password in pairs:
#     queries.append(f"('{password}',1,0,{user_id})")

# res = pattern + ', '.join(queries)

with open('bonuses.sql','w') as file:
    file.write(res)
