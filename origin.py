# 1. Количество разных источников сообщений. Предоставить перечень.
# 2. Количество разных типов сообщений от Cisco ASA, встречающихся в дампе. Предоставить
# перечень.
# 3. Перечень различных IP-адресов, встретившихся в сообщениях Cisco ASA.
#
# Что в этом файле показалось вам странным?
# Как вы можете объяснить эту «странность» (предложить гипотезы).
 
import re
 
 
class DataDetectionAutomation:
    ip_regexp = r'[0-9]+(?:\.[0-9]+){3}'
 
    #<174>Nov 13 15:39:17 ZOO-ML-CE backup PFE_FW_SYSLOG_IP: FW: ge-1/0/10.0  A  tcp 10.164.161.153 10.187.121.59  8082 43206 (2 packets)
    line_parser_regexp = r'^<\d*>Nov \d{2} \d{2}:\d{2}:\d{2} ([^: ]*) ([^:]*):(.*)$'
    replace_regexp = r'\1@\2@\3'
 
    def __init__(self, file_address):
 
        self.sources = set()
        self.message_types = set()
        self.ips = set()
 
        with open(file_address, 'r') as file:
            for i, line in enumerate(file.readlines()):
                if 'last message repeated' in line:
                    continue
 
                elems_in_line = re.sub(DataDetectionAutomation.line_parser_regexp,
                           DataDetectionAutomation.replace_regexp, line).split('@')
                print(elems_in_line)
 
                self.sources.add(elems_in_line[0])
 
                if not DataDetectionAutomation.is_from_Cisco_ASA(line):
                    continue 
 
                self.message_types.add(elems_in_line[1])
 
                for elem in re.findall(DataDetectionAutomation.ip_regexp, elems_in_line[2]):
                    if self.is_ip_valid(elem):
                        self.ips.add(elem)
    
    def is_from_Cisco_ASA(string):
        return " %ASA-" in string
 
    @staticmethod
    def is_ip_valid(ip):
        is_valid = True
        for elem in map(int, ip.split('.')):
            is_valid *= (0 <= elem < 256)
        return is_valid
 
 
dda = DataDetectionAutomation('./Log4test')
print("Количество разных источников сообщений ", len(dda.sources))
print(dda.sources)
print("Количество разных типов сообщений от Cisco ASA ", len(dda.message_types))
print(dda.message_types)
print("Перечень различных IP-адресов, встретившихся в сообщениях Cisco ASA", len(dda.ips))