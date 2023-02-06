from cryptography.fernet import Fernet
 
# we will be encrypting the below string.
password = "Enter_password"
 
# Generate new key
key = Fernet.generate_key()


# If key already generated, enter key in line below and uncomment.
# key = "iuuBv4sUyiwedoiuewrheoirhfer888jIOJOIUJvvAGEbdkCuVKXN-_B8g=".encode('ASCII) 

# Generate Fernet object with key
fernet = Fernet(key)

# Encrypt password string with key
encPassword = fernet.encrypt(password.encode())

# Decrypt password string with key
decPassword = fernet.decrypt(encPassword).decode()


# Save ENCRYPTED PASSWORD and KEY, do not generate several keys!
print("\n\nENCRYPTED PASSWORD, put it in users in grupprum_executable: ", encPassword,"\n")
 
print("DECRYPTED PASSWORD, check if correct: ", decPassword,"\n")

print ("KEY, save to windows credentials!: ", key.decode(),"\n\n")