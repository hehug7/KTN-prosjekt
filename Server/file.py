def saveusers(clients, filename):
    text = ""
    for user in clients:
        text += user + "," + str(clients[user]) # dette får jeg skrevet til tekst, men socket connection må konverteres her til str.
        #print(type(clients[user]), " her")
    f = open(filename,'w')
    f.write(text)
    f.close()

def loadusers(filename):
    db = {}
    f = open("users.txt")
    users = f.readlines()
    f.close()

# det skjer en feil her fordi user's connection er ikke av typen socket, men av typen string
    for user in users:
        db[user.split(",")[0]] = user.split(",")[1][:-1] # riktig = feil, der feil er connection på stringformat
        print(user.split(",")[1][:-1])
    return db

def savehistory(history, filename):
    text = ""
    for line in history:
        text += line + "\n"

    f = open(filename, 'w')
    f.write(text)
    f.close()

def loadhistory(filename):
    list = []

    f = open(filename, 'r')
    history = f.readlines()
    for line in history:
        list.append(line)
    return list

def load(filnavn):
    f = open(filnavn,'r')

    info = f.readlines()
    list = []

    for line in info:
        list.append(line)
    f.close()

    return list

