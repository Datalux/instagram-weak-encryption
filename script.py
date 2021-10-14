while(True):
    enc = input('Insert encrypted password: ')

    if(len(enc) < 3):
        print("Wrong input")
        continue

    c = enc.split(':')[3] if ':' in enc else enc
    cl = len(c)
    pad = (int)((cl / 4) - 36)
    pad1 = 1 if c[-1] == '=' else 0
    pad2 = 1 if c[-2] == '=' else 0
    pl = (len(c) - 136 - pad - pad1 - pad2)
    if(pl < 0):
        print("Wrong input")
    else:        
        print("Password len: " + str(pl))