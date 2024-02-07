# parsing test log file
# folders
#  seqN, Month, DayOfMonth, time(hh:mm:ss), Origin, node, action, chain, iface, Flag, proto, srcIP, dstIP, srcPort, dstPort, PacketCount 

import os
import re
import string

specials = '<>[]' #etc
trans = str.maketrans(specials, ' '*len(specials))


filename = "./Log4test"

Matrix = []

with open(filename) as file:
    lines = [line.rstrip().translate(trans) for line in file]

A = []

for line in lines:
    if (line.find("Deny") == -1 ) and ( line.find("failed") == -1):
        A.append(list(map(str, line.split(" "[4:]))))

OriginNones = [A[i][0] for i in range(len(A))]

#uniqs = set(uniqs)
print("Оригинальных источников: ", end=' ')
print(len(set(OriginNones)))
for uniq in set(OriginNones):
    print(uniq, end=' ')

print()

print("Типов сообщений, всего: ", end=' ')
 
OrigTypesMsg = [A[i][2] for i in range(len(A))]
print(len(set(OrigTypesMsg)))
for uniq in set(OrigTypesMsg):
    print("\t" + uniq) 

print("Уникальных IP, всего: ", end=' ')
OrigIP = [A[i][5] for i in range(len(A))]
print(len(set(OrigIP)))
for uniq in set(OrigIP):
    print("\t" + uniq) 




