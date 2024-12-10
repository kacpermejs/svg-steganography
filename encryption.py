import random

def characters_to_ascii_string(char_list):
    """
    Convert a list of characters into a string of their ASCII codes.

    Args:
        char_list (list): List of characters (e.g., ['a', 'b', '\0']).

    Returns:
        str: A string of ASCII codes joined by spaces (e.g., "97 98 0").
    """
    try:
        # Convert each character to its ASCII code
        ascii_codes = [f"{ord(char):03}" for char in char_list]
        # Join the ASCII codes into a single string
        return ''.join(ascii_codes)
    except TypeError:
        raise ValueError("Input must be a list of characters.")

def encrypt(message, seed, containerNumber, chunk_size):
  random.seed(seed)
  
  while len(message) < chunk_size:
    if isinstance(message, list):
      message.extend(['\0'])
    else:
      message.append(['\0'])
  
  keyLength = len(message)*3
  keyMin = pow(10, keyLength-1)
  keyMax = (keyMin * 10) - 1
  
  key = random.randint(keyMin, keyMax)
  
  print('key:')
  print(key)
  
  messageCode = 0
  messageCode = characters_to_ascii_string(message)
  
  # print('message:')
  # print(message)
  # print('ASCII message:')
  # print(messageCode)
  
  messageCodeEncrypted = int(messageCode) ^ key
  
  rounded_number_str = f"{round(containerNumber, 5):.5f}"
    
  encrypted_number_string_1 = rounded_number_str + str(messageCode)

  print(encrypted_number_string_1)

  encrypted_number_string = rounded_number_str + str(messageCodeEncrypted)
  return encrypted_number_string
  
def decrypt(seed, encrypted_number_string, chunk_size):
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
  
  decrypted_code = int(message_code_encrypted) ^ key
  
  decrypted_str = f"{decrypted_code:09d}"
  
  message = ''.join(chr(int(decrypted_str[i:i+chunk_size])) for i in range(0, chunk_size*3, chunk_size))

  return message