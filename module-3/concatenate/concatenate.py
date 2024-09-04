# Exercise Task Concatenate
# 1
a = "Developer"
b = "Akademie"
c = '.'
d = "com"

print(a + b)            # DeveloperAkademie
print(a + b + c + d)    # DeveloperAkademie.com
print(a + b - c)        # Syntax Error - no subtract
print(5 * c)            # .....
print("3d")#no quotes   # Syntax Error
print(a + d)            # Developercom
print(a + b + d)        # DeveloperAkademiecom
print(d**2)             # TypeError
print(2 * (c + d))      # .com.com
print(3 * c + 2 * d)    # ...comcom
