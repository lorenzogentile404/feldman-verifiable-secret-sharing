import random
import math

# Reference https://profs.info.uaic.ro/~siftene/Feldman.pdf

# Helper function
def isprime(n):
    if n == 2:
       return True
    if n == 1 or n % 2 == 0:
        return False    
    i = 3    
    while i <= math.sqrt(n):
        if n % i == 0:
            return False
        i = i + 2        
    return True 

# Pick q, p primes such that q | p - 1, that is equvalent to
# say that p = r*q + 1 for some r

# Choose q
while True:
    q = 127 #int(input("Insert a prime q: "))
    if isprime(q):
        break
 
print("q = " + str(q))
print("\nq is prime\n")

# Find p and r
r = 1
while True:
    p = r*q + 1
    if isprime(p):
        print("r = " + str(r))
        print("p = " + str(p))
        print("\np is prime\n")
        break
    r = r + 1

# Compute elements of Z_p*
Z_p_star = []
for i in range(0, p):
    if(math.gcd(i,p) == 1):
        Z_p_star.append(i)

print("Z_p* = ")
print(Z_p_star)

# Compute elements of G = {h^r mod p | h in Z_p*}
G = [] 
for i in Z_p_star:
    G.append(i**r % p)

G = list(set(G))
G.sort()
print("\nG = ")
print(G)
print("Order of G is " + str(len(G)) + ". This must be equal to q.")        

# Since the order of G is prime, any element of G except 1 is a generator
g = random.choice(list(filter(lambda g: g != 1, G)))
print("\ng = " + str(g))

# Secret taken from the group Z_q* 
while True:
    a0 = 84 #int(input("Inser a secret in Z_q*: "))
    if a0 >= 1 or a0 <= q:
        break

# Secret polynomium coefficients taken from the group Z_q*
a1 = random.randint(1, q)
a2 = random.randint(1, q)

a = [a0, a1, a2]

print("The secret polynomium is: " + str(a0) + " + " +  str(a1) + "x + " + str(a2) + "x^2")

# The function f is a polynomium from the group Z_q* (for simplicity 2nd degree is considered)
def f(x):
    return ((a0 + a1*x + a2*x**2) % q)

# List of shares
s = []

# Compute shares and verify
# Note that P_i receives as a share s = f(i)
# In general, each party P_1,...,P_6 could receive a different arbitrary share
for i in range(1,7):
    print("\ni = " + str(i))
    s.append(f(i))
    print("Share: f(" + str(i) + ") = " + str(f(i)))
    print("Commitment: g^f(" + str(i) + ") = " + str(g**f(i) % p))
    print("Verification: (g^a0)*((g^a1)^i)*((g^a2)^(i^2)) = " + str((g**a0)*((g**a1)**i)*((g**a2)**(i**2)) % p) + "\n") 

# Print shares
print(s)

# Parties cooperating to reconstruct the secret
B = [1,2,3]

def delta(i):
    d = 1
    print("\ni= ")
    print(i)
    for j in B:
        if j != i:
            print("\nj= ")
            print(j)
            d *= -j/(i - j)
    print("delta = " + str(d % q))
    return d

a0_reconstructed = 0
for i in B:
    print("Share of P_" + str(i) + " is " + str(s[i - 1]))
    a0_reconstructed += delta(i)*s[i - 1]

print(a0_reconstructed % q)
