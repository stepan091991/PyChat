import rsa
#Боб формирует публичный и секретный ключ

(bob_pub, bob_priv) = rsa.newkeys(1024)

#Алиса формирует сообщение Бобу и кодирует его в UTF8,
#поскольку RSA работает только с байтами
message = 'hello Bob!'.encode('utf8')

#Алиса шифрует сообщение публичным ключом Боба
crypto = rsa.encrypt(message, bob_pub)
print(crypto)
#Боб расшифровывает сообщение своим секретным ключом
message = rsa.decrypt(crypto, bob_priv)
print(message.decode('utf8'))