import random

def isProbablyPrime(n, rounds=1000):    
        n = int(n)
        if(n < 2):
                return 1
        if(n == 2):
                return True
        if((n != 2) and ((n%2)==0)):
                return False
        m = n-1
        k = 0
        while((m%2)==0):
                m/=2
                k+=1
        assert(2**k * m == n-1)        
        
        round_num = 0; 
        while(round_num < rounds):
                a = random.randrange(2, n-2)
                b = pow(a, m, n)
                if(b % n == 1 or b % n == -1):
                        return True 
                else:
                        iterations = 0
                        def try_composite(b, i):
                                i+=1
                                b = (pow(b, 2, n))
                                if(b % n == 1):
                                        return False
                                elif(b % n == -1):
                                        return True
                                else:
                                        if(i < k):
                                                try_composite(b, i)
                                        else:
                                                return False
                        result = try_composite(b, iterations)
                round_num+=1
        if(result == True):
                return True
        else:
                return False        

def getProbablePrime(bit_length, num_rounds=5000):
        random_num = random.getrandbits(bit_length)
        while(isProbablyPrime(random_num, num_rounds) == False):
                random_num = random.getrandbits(bit_length)
                isProbablyPrime(random_num, num_rounds)
        return random_num
    
def gcd(a, b):
        if(a < b):
                t = a
                a = b
                b = t
                
        r = a % b #remainder
        #Eucledian algorithm
        def eucledian(b, r):
                if(r == 0):
                        gcd = b
                        return gcd
                else:
                        temp = r
                        r = b % r
                        b = temp            
                        ans = eucledian(b, r)
                        return ans
        gcd = eucledian(b, r)
        return gcd
    
def multiplicativeInverse(a, b):
        def egcd(a, b):
                if (a == 0):
                        return (b, 0, 1)
                else:
                        g, y, x = egcd(b % a, a)
                        return (g, x - (b // a) * y, y)
        def multInv(a, n):
                gcd, x, y = egcd(a, n)
                if (gcd != 1):
                        return None
                else:
                        return x % n
        multInv_ =  multInv(a, b)
        return multInv_
    
def generateRSAkeyPair(bit_lenght):
        p = getProbablePrime(bit_lenght)
        q = getProbablePrime(bit_lenght)
        n = p * q 
        phi_n = (p-1)*(q-1)
        e = random.randrange(3, phi_n)
        def gete(e, temp):
                gcd_ = gcd(e, temp)
                if(gcd_ != 1):
                        ran = random.randrange(3, phi_n)
                        e = gete(ran, temp)
                        #return e
                else:
                        return e
        e = gete(e, phi_n)
        
        def getd():
                d = multiplicativeInverse(e, phi_n)
                return d
        d = getd()
        
        #Write public and private key files
        write_file("public", (n, e), 1)
        write_file("private", (n, d), 1)
        
        print "p = %d" % p
        print "q = %d" % q   
        print "e = %d" % e   
        print "d = %d" % d   
        
        print "Generated files: public.txt, private.txt"        
        
        return p * q, e, d

def RSAencrypt(m, pk):
        n = pk[0]
        e = pk[1]
        c = pow(m, e, n)
        print "Encrypted message: %s (saved to encrypted.txt)" % c
        write_file("encrypted", str(c), 0)


def RSAdecrypt(c, prk):
        n = prk[0]
        d = prk[1]   
        m = pow(c, d, n)
        print "Decrypted message: %s" % m

def pohligHellman(a, p, b):
        #check if p is prime
        if(isProbablyPrime(p)):
                pass
        else:
                print "%d is not prime" % p
                return None
        
        #Find prime factors of p-1
        n = p - 1
        
        #Count how many times each factor is repeated
        pairs = countFactors(factor(n))
        
        def findXs(a, b, p, q, r):
                #First exponent
                exp_ = (p - 1)/q
                b_curr = b
                x_new = 0
                a_new = pow(a, exp_, p)
                q_ = 1
                
                a_inv = multiplicativeInverse(a, p)
                
                for i in range(0, r):
                        b_new = pow(b_curr, exp_, p)
                        def xTest(a, b, p):
                                a_x = 1
                                b %= p
                                for i in range(p - 1):
                                        if a_x == b: 
                                                return i
                                        a_x = a_x * a % p
                                return None
                        x = xTest(a_new, b_new, p)
                        x_new+=x*q_
                        
                        #Next beta
                        b_curr = b_curr * pow(a_inv, x * q_, p) % p
                        q_ *= q
                        exp_ /= q
                return(x_new, q_)
        
        #Find congruences (x, q^(number of repetitions))
        congruences = [] 
        for (q, r) in pairs:
                congruences.append(findXs(a, b, p, q, r))
        
        #Combine resulting congruences to obtain answer
        ans = CRT(congruences)
        return ans
        
        

'''

These are supporting functions

'''

def read_input(message):
        input_ = raw_input(message)
        try:
                val = int(input_)
        except ValueError:
                print("(!)Error, not an integer")
                raise SystemExit
        return int(input_)

def read_file(message):
        file_ = raw_input(message)
        file_ = open(file_, 'r')
        n, e = file_.read().split("::", 2)
        return int(n), int(e)

def write_file(name, args, flag):
        if(flag == 1):
                file_ = open(name + ".txt", 'w')
                file_.write(str(args[0]) + "::" + str(args[1]))
        else:
                file_ = open(name + ".txt", 'w')
                file_.write(args)

def factor(n):
        k = 2
        factors = []
        while (n > 1):
                if(n % k == 0):
                        factors.append(k)
                        n/=k
                else:
                        k+=1+k%2
        return factors

def countFactors(list_):
        current = NotImplemented
        n = 0
        pairs = []
        for x in list_:
                if x == current:
                        n += 1
                else:
                        if n > 0:
                                pairs.append((current, n))
                        n = 1
                        current = x
        pairs.append((current, n))
        return pairs

def CRT(congruences):
        M = 1
        i = 0
        for (a, b) in congruences:
                M *= b
        for (a, b) in congruences:
                m = M/b
                i += a * multiplicativeInverse(m, b) * m
        ans = i % M
        return ans

def xgcd(a,b):
        """Extended GCD:
        Returns (gcd, x, y) where gcd is the greatest common divisor of a and b
        with the sign of b if b is nonzero, and with the sign of a if b is 0.
        The numbers x,y are such that gcd = ax+by."""
        prevx, x = 1, 0;  prevy, y = 0, 1
        while b:
                q, r = divmod(a,b)
                x, prevx = prevx - q*x, x  
                y, prevy = prevy - q*y, y
                a, b = b, r
        return a, prevx, prevy