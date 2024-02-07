# parsing test log file
# folders
#  seqN, Month, DayOfMonth, time(hh:mm:ss), Origin, node, action, chain, iface, Flag, proto, srcIP, dstIP, srcPort, dstPort, PacketCount 

import os
import re
import string

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

specials = '<>[]' #etc
trans = str.maketrans(specials, ' '*len(specials))

filename = "./Log4test"

Matrix = []

with open(filename) as file:
    lines = [line.rstrip().translate(trans).replace("%", "% ") for line in file]

A = []

OrigIP = set()

for line in lines:
    A.append(list(map(str, line.split()[4:])))


for i in A[4:]:
    for j in i:
        if validate_ip(j):
            OrigIP.add(j)


OriginNodes = [A[i][0] for i in range(len(A))]


print("Оригинальных источников: ", end=' ')
print(len(set(OriginNodes)))
for uniq in set(OriginNodes):
    print("\t" + uniq)

print()

OrigTypesMsg = set()

print("Типов сообщений, всего: ", end=' ')

for r in [A[i][2] for i in range(len(A))]:
    match = re.search(r"ASA-\d", r)
    if match != None:
        OrigTypesMsg.add(match.group(0))
print(len(set(OrigTypesMsg)))
for uniq in OrigTypesMsg:
    print("\t", end=' ')
    print(uniq) 

print("Уникальных IP, всего: ", end=' ')
print(len(OrigIP))
#for j in set(OrigIP):
#    print(j)



