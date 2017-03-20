"""
MESSAGE DECODING
CHALLENGE DESCRIPTION:

Credits: This challenge has appeared in a past ACM competition.

Some message encoding schemes require that an encoded message be sent in two parts.
The first part, called the header, contains the characters of the message.
The second part contains a pattern that represents the message.
You must write a program that can decode messages under such a scheme.

The heart of the encoding scheme for your program is a sequence of "key"
strings of 0's and 1's as follows:

0,00,01,10,000,001,010,011,100,101,110,0000,0001,. . .,1011,1110,00000, ...

The first key in the sequence is of length 1, the next 3 are of length 2,
the next 7 of length 3, the next 15 of length 4, etc. If two adjacent keys
have the same length, the second can be obtained from the first by adding 1 (base 2).
Notice that there are no keys in the sequence that consist only of 1's.

The keys are mapped to the characters in the header in order. That is,
the first key (0) is mapped to the first character in the header,
the second key (00) to the second character in the header,
the kth key is mapped to the kth character in the header.

For example, suppose the header is:

AB#TANCnrtXc
Then 0 is mapped to A, 00 to B, 01 to #, 10 to T, 000 to A, ..., 110 to X, and 0000 to c.

The encoded message contains only 0's and 1's and possibly carriage returns,
which are to be ignored. The message is divided into segments. The first 3
digits of a segment give the binary representation of the length of the keys
in the segment. For example, if the first 3 digits are 010, then the remainder
of the segment consists of keys of length 2 (00, 01, or 10). The end of the
segment is a string of 1's which is the same length as the length of the keys
in the segment. So a segment of keys of length 2 is terminated by 11. The entire
encoded message is terminated by 000 (which would signify a segment in which the
keys have length 0). The message is decoded by translating the keys in the
segments one-at-a-time into the header characters to which they have been mapped.

https://www.codeeval.com/browse/36/

"""

import sys
import math

BINARY_CHAR = ('0', '1')


def string_fill(value, char, n):
    return '%s%s' % (char * (n - len(value)), value)


class Challenge36:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        """lee el archivo desde path_file"""
        assert self.file_path is not None, '`file_path` is required'
        f = open(self.file_path, 'r')
        return f.readlines()

    def get_keys(self, length):
        """genera las claves"""
        i = 1
        count = 0
        keys = []
        while True:
            count_sequence = self.get_sequence(i)
            count += count_sequence
            for j in range(0, count_sequence):
                binary_int = format(j, 'b')
                key = string_fill(binary_int, '0', i)
                keys.append(key)
            if count >= length:
                break
            i += 1
        return keys[:length]

    def get_sequence(self, length):
        """genera la secuencia"""
        i = 0
        for k in range(0, length):
            j = math.pow(2, k)
            i = j + i
        return int(i)

    def split_message(self, binary_message, limit):
        """
        Devuelve la parte binaria y el mensaje restante:
        return (binary_part, binary_message)
        """
        return binary_message[:limit], binary_message[limit:]

    def mapping_keys(self, values, inverse=False):
        """mapea las claves"""
        length = len(values)
        keys_range = range(0, length)
        keys = self.get_keys(length)

        if inverse:
            return {values[i]: keys[i] for i in keys_range}
        return {keys[i]: values[i] for i in keys_range}

    def encode_message(self, message):
        """Encode message"""
        if BINARY_CHAR in message:
            raise ValueError, '`0` and `1` not allowed in message'

        chars = [char for char in message]
        unique_chars = list(set([char for char in message]))
        mapping = self.mapping_keys(unique_chars, inverse=True)

        encode_messsage = []
        encode_messsage += unique_chars

        for i, char in enumerate(chars):
            key_char = mapping[char]
            key_length = len(key_char)

            last_key_length = len(mapping[chars[i - 1]]) if i - 1 < 0 else None
            next_key_length = len(mapping[chars[i + 1]]) if i + 1 < len(chars) else None

            binary_length = format(key_length, 'b')
            p1 = string_fill(binary_length, '0', 3)

            if last_key_length != key_length:
                encode_messsage.append(p1)

            encode_messsage.append(key_char)

            if next_key_length != key_length:
                encode_messsage.append('1' * key_length)

        encode_messsage.append('000')
        return ''.join(encode_messsage)

    def decode_message(self, message_encode):
        """Decode message"""
        message_encode = message_encode.rstrip()
        encoded = ''.join([char for char in message_encode if char in BINARY_CHAR])
        headers = [header for header in message_encode if header not in BINARY_CHAR]
        mapping = self.mapping_keys(headers)

        if len(encoded) <= 3:
            raise ValueError, '`encoded_message` is invalid'

        decode_messsage = []

        while True:
            binary_length, encoded = self.split_message(encoded, 3)
            key_length = int(binary_length, 2)
            binary_part = None

            while True:
                binary_part, encoded = self.split_message(encoded, key_length)
                if binary_part == '1' * key_length:
                    break
                else:
                    decode_messsage.append(mapping[binary_part])
            if len(encoded) <= 3:
                break

        return ''.join(decode_messsage)

    def play(self):
        lines = self.read_file()
        for line in lines:
            print self.decode_message(line)


if __name__ == '__main__':
    path_file = sys.argv[1]
    challenge = Challenge36(path_file)
    challenge.play()
    # print challenge.encode_message('http://www.crehana.com')
