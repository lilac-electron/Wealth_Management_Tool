from passlib.hash import sha256_crypt
var1 =  (sha256_crypt.hash("test6@test.com"))
print (sha256_crypt.verify("test6@test.com", var1))