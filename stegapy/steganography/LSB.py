from stegapy.models.stega import BaseSteganography
import struct


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
        msg_bits = self.__to_bits(msg.read())
        # Preparing key (length of message)
        key = struct.pack('I', int(len(msg_bits)/8))
        key = self.__to_bits(key)
        header_samples = [byte for byte in self.container.content[:44]]
        # Include key in container data
        key_samples = self.__samples_encoding(key, limit=len(key))
        # Include message in container data
        encoded_samples = self.__samples_encoding(msg_bits, len(key_samples),
                                                  len(msg_bits))
        # Prepare contaminated data
        out_samples = bytes(header_samples + key_samples + encoded_samples)
        out_samples = out_samples + self.container.content[len(out_samples):]

        return out_samples

    def decode(self):
        """Decode method"""
        samples = self.container.read()
        # 32 is size of key
        key_samples = samples[:32]
        content_samples = samples[32:]

        # Reach key data
        key = self.__samples_decoding(key_samples, 4)
        key = int(struct.unpack('I', key)[0])

        # Reach message data
        content_data = self.__samples_decoding(content_samples, key)
        return content_data