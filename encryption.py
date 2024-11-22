import random

def encrypt(message, seed, containerNumber):
  random.seed(seed)
  
  keyLength = len(message)*3
  keyMin = pow(10, keyLength-1)
  keyMax = (keyMin * 10) - 1
  
  key = random.randint(keyMin, keyMax)
  
  print('key:')
  print(key)
  
  messageCode = 0
  i = 0
  
  for character in message:
    messageCode += ord(character) * pow(10, i)
    i += 3
  
  print('message:')
  print(message)
  print('ASCII message:')
  print(messageCode)
  
  messageCodeEncrypted = messageCode ^ key
    
  encrypted_number_string_1 = str(round(containerNumber, 5)) + str(messageCode)

  print(encrypted_number_string_1)

  encrypted_number_string = str(round(containerNumber, 5)) + str(messageCodeEncrypted)
  return encrypted_number_string
  
def decrypt(seed, encrypted_number_string):
  dot_index = encrypted_number_string.find('.')

    # Sprawdź, czy kropka istnieje w ciągu
  if dot_index != -1:
        # Ucinamy wszystko do kropki i 5 znaków po niej
      message_code_encrypted = encrypted_number_string[dot_index + 6:]

  random.seed(seed)
  
  keyLength = len(message_code_encrypted)
  keyMin = pow(10, keyLength-1)
  keyMax = (keyMin * 10) - 1;
  
  key = random.randint(keyMin, keyMax)
  
  print('key:')
  print(key)

  return int(message_code_encrypted) ^ key