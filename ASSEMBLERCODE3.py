import re
LC = 0
tokens = list()
code = open("ALPCODE1.txt",encoding="utf-8")
line = code.readlines()
for i in line:
    k = i.rstrip('\n')
    k = re.split(' |,',k)
    tokens.append(k)
    
for i in tokens:
    for j in i:
        if(j==''):
            i.remove(j)
final_tokens = [x for x in tokens if x!=[]]

MOT = ['STOP','ADD','MULT','MOVER','MOVEM','COMP','BC','DIV','TRANS',
      'READ','PRINT','START','END','ORIGIN','EQU','LTORG','DS','STORE','BC'
       'DC','AREG','BREG','CREG','EQ','LT','GT','LE','GE','NE','ANY','LOAD','SUB']
fdict_sym = dict()
fdict_lit = dict()
sym_indexc = 0
lit_indexc = 0
pool_variable = 0


symtab = PrettyTable(['INDEX NO.','SYMBOL','ADDRESS'])
littab = PrettyTable(['INDEX NO.','LITERAL','ADDRESS'])
pooltab = PrettyTable(['LITERAL NUMBER'])



LC = int(final_tokens[0][1])
# print(final_tokens)
for i in range(1,len(final_tokens)):
    m = re.search("(=(‘[0-9]+’))",final_tokens[i][-1])
    if(final_tokens[i][0]!='END'):
        if(final_tokens[i][0]!='LTORG'):
            if(final_tokens[i][0] not in MOT and  m!=None ):
                if(final_tokens[i][1]!='EQU'):
                    key = final_tokens[i][0]
                    if key in fdict_sym.keys():
                        fdict_sym[final_tokens[i][0]][0]=LC
                    else:
                        fdict_sym[final_tokens[i][0]]=[LC,sym_indexc]
                        sym_indexc = sym_indexc + 1
                    if m.group() not in fdict_lit.keys():
                        fdict_lit[final_tokens[i][-1]]=[0,lit_indexc]
                        lit_indexc = lit_indexc + 1
                    LC=LC+1
                elif(final_tokens[i][1]=='EQU'):
                    p=final_tokens[i][2]
                    if(len(p)<1):
                            fdict_sym[final_tokens[i][0]][0]=fdict_sym[p[0]][0]
                    else:
                        p=re.split("\+|-",p)
                        x = p[0]
                        globals()[x] = fdict_sym[p[0]]
                        LC1 = eval(final_tokens[i][2])
                        fdict_sym[final_tokens[i][0]]=LC1
            elif(final_tokens[i][0] not in MOT ):
                if(final_tokens[i][1]!='EQU'):
                    key = final_tokens[i][0]
                    if key in fdict_sym.keys():
                        fdict_sym[final_tokens[i][0]][0]=LC
                    else:
                        fdict_sym[final_tokens[i][0]]=[LC,sym_indexc]
                        sym_indexc = sym_indexc + 1
                    LC=LC+1
                elif(final_tokens[i][1]=='EQU'):
                    p=final_tokens[i][2]
                    if(len(p)<1):
                            fdict_sym[final_tokens[i][0]][0]=fdict_sym[p][0]
                    else:
                        p=re.split("\+|-",p)
                        x = p[0]
                        globals()[x] = fdict_sym[p[0]][0]
                        LC1 = eval(final_tokens[i][2])
                        fdict_sym[final_tokens[i][0]][0]=LC1
            elif(m!=None):
                fdict_lit[m.group()] =[0,lit_indexc]
                lit_indexc = lit_indexc + 1
                LC=LC+1
            elif(final_tokens[i][0]=='ORIGIN'):
                p=final_tokens[i][1]
                if(len(p)<1):
                    fdict_sym[final_tokens[i][0]][0]=fdict_sym[p][0]
                else:
                    p=re.split("\+|-",p)
                    x = p[0]
                    globals()[x] = fdict_sym[p[0]][0]
                    LC = eval(final_tokens[i][1])      
            elif(final_tokens[i][0]!='ORIGIN'):
                st = final_tokens[i][-1]
                if(st not in fdict_sym.keys()):
                    r = re.search("[A-Z]+",st)
                    if(final_tokens[i][-1] not in MOT and bool(r) ):
                        fdict_sym[final_tokens[i][-1]]=[0,sym_indexc]
                        sym_indexc = sym_indexc + 1
                LC=LC+1
        else:
            pooltab.add_row([pool_variable])
            print(fdict_lit,LC)
            for key in fdict_lit.keys():
                fdict_lit[key][0] = LC
                LC = LC+1
            for l,a in fdict_lit.items():
                littab.add_row([a[1],l,a[0]])
                pool_variable = pool_variable+1
            fdict_lit.clear()
    else:
        if bool(fdict_lit):
            pooltab.add_row([pool_variable])
        for key in fdict_lit.keys():
            fdict_lit[key][0] = LC
            LC = LC+1
            


print("SYMBOL TABLE")
for s,a in fdict_sym.items():
    symtab.add_row([a[1],s,a[0]])
print(symtab)
print("LITERAL TABLE")
for l,a in fdict_lit.items():
    littab.add_row([a[1],l,a[0]])
print(littab)
print("POOL TABLE")
print(pooltab)