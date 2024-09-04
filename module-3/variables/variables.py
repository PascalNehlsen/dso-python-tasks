# Exercise Task Variables
# 2
vorname = " Mustermann"
nachname = "Max"

vorname, nachname = nachname, vorname 
print (vorname + nachname)

# 3
a = 42
b = a
c = a
a = 10
b = c
print(a) # 10
print(b) # 42
print(c) # 42

# 4 
vorname = "Misa"
nachname = "Amani"
geschlecht = "weiblich"
tag = 22
monat = "September"
jahr = "1998"

print (f"""Mein name ist {vorname} {nachname}. \nIch bin {geschlecht} und wurde am {tag}. {monat} {jahr} geboren.""")