class Encryption:
    
    def __init__(self,data):
        self.password = 42
        self.data = data

    def xor_encryption(self):
        xored_array = []
        for word in (self.data):
            if len(word)>1:
                for letter in word:
                    xored_character = ord(letter) ^ self.password
                    xored_array.append(chr(xored_character))
            elif word == " " :
                xored_array += " " 
            else:         
                xored_character = ord(word) ^ self.password
                xored_array += chr(xored_character)     
        return xored_array