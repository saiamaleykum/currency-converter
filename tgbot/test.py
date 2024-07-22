lst = """ZAR
BYN
AMD
TRY
JPY
KRW
VND
GEL
XDR
CZK
NZD
GBP
TMT
EGP
AED
TJS
SGD
PLN
KGS
CAD
RSD
INR
RON
EUR
AUD
THB
QAR
IDR
USD
CNY
NOK
HKD
DKK
MDL
AZN
SEK
KZT
BRL
CHF
UAH
HUF
UZS
BGN"""

lst = lst.split('\n')

CONST = 10

for i in range(len(lst)):
    print(lst[i])
    if (i + 1) % CONST == 0:
        print('')

print('\n-------\n')

def get_msg(lst: list, page: int):
    temp_lst = lst[page*CONST:(page+1)*CONST]
    for cur in temp_lst:
        print(cur)

get_msg(lst, 4)
