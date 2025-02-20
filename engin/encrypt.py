class Encryption:
    def _init_(self):
        self.password = 42

    def xor_encryption(self, data):
        xored_string = ""
        for i, char in enumerate(data):
            xored_character = ord(char) ^ self.password
            xored_string += chr(xored_character)
        return xored_string

    def xor_decryption(self, data):
        xored_string = ""
        for i, char in enumerate(data):
            xored_character = ord(char) ^ self.password
            xored_string += chr(xored_character)
        return xored_string