import math
from functions import *
#from other_func import *


def Main():
    print "1. Miller Rabine (primarily test)\n2. Get a probably prime number\n3. Calculate GCD\n4. Calculate multiplicative inverse\n5. Generate RSA key pair\n6. RSA encrypt\n7. RSA decrypt\n8. Pohlig Hellman (returns x)"
    
    o = raw_input("Please enter an option: ")
    ##Fix interface for 1
    if(o == '1'):
        num = read_input("Enter number to check if it is prime: ")
        num = isProbablyPrime(num)
        if num == False:
            print "Composite"
        if num == True:
            print "Probably prime"
    ####
    elif(o == '2'):
        bit_length = read_input("Enter number of bits: ")
        num_rounds = read_input("Enter number of rounds: ")          
        getProbablePrime(bit_length, num_rounds)
        print "%d is probably prime" % getProbablePrime(bit_length, num_rounds) 
    elif(o == '3'):
        a = read_input("Enter number 1: ")
        b = read_input("Enter number 2: ")        
        print "gcd(%d, %d) = %d" % (a, b, gcd(a, b))
    elif(o == '4'):
        a = read_input("Enter number 1: ")
        b = read_input("Enter number 2: ")
        print "%d^-1 congruent %d = %d" % (a, b, multiplicativeInverse(a, b))
    elif(o == '5'):
        bit_length = read_input("Enter bit length: ")
        generateRSAkeyPair(bit_length)
    elif(o == '6'):
        message = read_input("Enter message to encrypt: ")
        pk_info = read_file("Enter public key information (file name, format n::e): ")
        if(int(math.log(pk_info[0])) < int(math.log(message))):
            print "Please generate a key with a larger number of bits"
            raise SystemExit
        RSAencrypt(message, pk_info)
    elif(o == '7'):
        ciphertext = read_input("Enter ciphertext to decrypt: ")
        prk_info = read_file("Enter private key information (file name, format n::d): ")
        RSAdecrypt(ciphertext, prk_info)            
    elif (o == '8'):
        g = read_input("Enter generator: ")
        p =  read_input("Enter prime: ")
        y = read_input("Enter y value: ")
        print "x is equal to: %d" % pohligHellman(g, p, y)
    else:
        print "Option is not valid"

if __name__ == '__main__':
    Main()