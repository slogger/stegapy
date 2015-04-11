from stegapy.models.stega import BaseSteganography
from stegapy.md5 import md5
from stegapy.errors import ContainerError
import struct
import gzip


class LSB(BaseSteganography):
    """Steganography in LSB method tool"""

    def __samples_encoding(self, bits, offset=0, limit=False):
        """Write necessary to us data in the least significant bits"""
        if bool(limit):
            samples = self.container.content[44+offset:44+offset+limit]
        else:
            samples = self.container.content[44+offset:]
        encoded_samples = []
        pos = 0
        for sample in samples:
            encoded_sample = sample
            if pos < len(bits):
                encode_bit = bits[pos]
                if encode_bit:
                    encoded_sample = sample | encode_bit
                elif (sample & 1):
                    encoded_sample = sample - 1
                pos += 1
            encoded_samples.append(encoded_sample)
        return encoded_samples

    def __samples_decoding(self, samples, length):
        """Get data in the least significant bits"""
        decoded_samples = []
        for pos in range(length):
            byte_samples = samples[(pos * 8):((pos+1) * 8)]
            byte = 0
            for (sample, i) in zip(byte_samples, range(0, 8)):
                byte = byte + ((sample & 1) * (2**i))
            decoded_samples.append(byte)
        return bytes(decoded_samples)

    def __to_bits(self, _bytes, nbits=8):
        """Convert bytes in bits"""
        bits = []
        for byte in _bytes:
            for i in range(nbits):
                bits.append((byte & (2 ** i)) >> i)
        return bits

    def encode(self, msg):
        """Encode method"""
        if len(self.container.read()) // 8 < msg.length:
            raise OverflowError("Too much data")
        checksum = md5(msg.read())
        checksum = struct.unpack(
            "{}b".format(len(checksum)), bytes(checksum, 'UTF-8'))
        msg_bits = self.__to_bits(msg.read())

        # Preparing key (length of message)
        key = struct.pack('I', int(len(msg_bits)/8))
        key = self.__to_bits(key)
        header_samples = list(self.container.content[:500])

        # Include key in container data
        key_samples = self.__samples_encoding(key, limit=len(key))

        # Prepare checksum
        checksum_bits = self.__to_bits(bytes(checksum))
        checksum_samples = self.__samples_encoding(
            checksum_bits,
            len(key_samples),
            len(checksum_bits)+len(key_samples)
            )

        # Include message in container data
        encoded_samples = self.__samples_encoding(
            msg_bits,
            len(key_samples) + len(checksum_samples),
            len(msg_bits))

        # Prepare contaminated data
        out_samples = bytes(
            header_samples +
            key_samples +
            checksum_samples +
            encoded_samples)
        out_samples += self.container.content[len(out_samples):]
        return out_samples

    def decode(self):
        """Decode method"""
        samples = self.container.read()
        KEY_LENGTH = 32
        CHECKSUM_LENGTH = 288

        key_samples = samples[:KEY_LENGTH]
        checksum_samples = samples[KEY_LENGTH:CHECKSUM_LENGTH]
        content_samples = samples[CHECKSUM_LENGTH+KEY_LENGTH:]

        # Reach key data
        key = self.__samples_decoding(key_samples, 4)
        key = int(struct.unpack('I', key)[0])

        # Get original checksum
        origin_checksum = self.__samples_decoding(checksum_samples, 32)
        origin_checksum = str(origin_checksum, 'UTF-8')

        # Reach message data
        content_data = self.__samples_decoding(content_samples, key)

        checksum = md5(content_data)
        if checksum == origin_checksum:
            return gzip.decompress(content_data)
        else:
            raise ContainerError("Container is broken")
