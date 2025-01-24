from collections import deque
import math
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
  
  keyLength = 3
  keyMin = pow(10, keyLength-1)
  keyMax = (keyMin * 10) - 1;
  
  key = random.randint(keyMin, keyMax)
  
  
  message = ''
  for i in range(0, len(message_code_encrypted), 3):
    group = message_code_encrypted[i:i+3]
    
    decrypted_code = int(group) ^ key
  
    decrypted_str = f"{decrypted_code:03d}"
  
    message = message + (chr(int(decrypted_str)))

  return message

def round_to_percent(value, percent=1):
    if value == 0:
        return 0  # No rounding needed for zero
    # Calculate 1% of the value
    precision = -int(math.log10(value * percent / 100))
    return round(value, precision)

def pad(num, nPlaces):
    """
    Pads the given number string to nPlaces decimal places.

    Parameters:
        number_str (str): The input string representing a number.
        nPlaces (int): The number of decimal places to pad to.

    Returns:
        str: The padded number as a string.
    """
    try:
        
        # Format the number to the required decimal places
        format_string = f"{{:.{nPlaces}f}}"
        return format_string.format(num)
    except ValueError:
        raise ValueError("Invalid input: The number_str must be a valid number string.")

def encrypt2(message: deque[list], seed, containerNumber):
  random.seed(seed)
  
  keyLength = 3
  keyMin = pow(10, keyLength-1)
  keyMax = (keyMin * 10) - 1
  
  key = random.randint(keyMin, keyMax)
  
  print('key:')
  print(key)
  
  number_to_save = str(containerNumber)
  rounded = round_to_percent(containerNumber, 1)
  encrypted_number_string = str(pad(rounded, 5))
  
  while True:
    character = message[0]

    messageCode = 0
    messageCode = characters_to_ascii_string(character)
    
    encrypted_code = int(messageCode) ^ key;

    encrypted_number_string = encrypted_number_string + str(encrypted_code)
    
    if not ((str(float(encrypted_number_string)) == encrypted_number_string) and (round_to_percent(float(encrypted_number_string), 1) == rounded)):
      break
    message.popleft()
    number_to_save = encrypted_number_string
    if (len(message) == 0):
      break
  
  return number_to_save, message
