"""WAV container

Copyright 2014 Maxim Syrykh
"""

from stegapy.models.container import BaseContainer
from stegapy.errors import InputError
from stegapy.errors import ContainerError
import struct


class WAV(BaseContainer):
    """WAV container class"""

    def __init__(self, path, read=True, valid=True):
        """Base init wav container parser

        Arguments:

            path – path to file
            read – flag: nead read file?
        """
        self.name = path
        if read:
            self.file_read()
            self.read_param()
            if valid:
                self.is_valid()

    # We only support this WAV formats
    audio_format_table = {
        0x0001: 'PCM/uncompressed'
    }

    def file_read(self):
        """File reader method"""
        try:
            with open(self.name, "rb") as f:
                self.content = f.read()
        except FileNotFoundError:
            raise InputError("File not found")
        except Exception:
            raise InputError()

    def is_valid(self):
        """Validate function"""
        if self.chunk_id != b'RIFF':
            raise ContainerError('chunk_id should be RIFF!')
        elif self.chunck_format != b'WAVE':
            raise ContainerError('Container is not WAV')
        elif self.fmt_subchunk_size != 16:
            raise ContainerError
        elif self.block_align != self.num_channels * self.bits_sample/8:
            raise ContainerError("Mismatch data fmt_subchunk")
        elif self.length == 0:
            raise InputError('File %s is empty!' % (self.name))
        else:
            return True

    def get_params(self, ignored=[]):
        """If you need all container params, just call me

        Arguments:

            ignored – list ignired params
        """
        params = {
            'chunk_id': self.chunk_id,
            'chunk_size': self.chunk_size,
            'chunck_format': self.chunck_format,
            'fmt_subchunk_id': self.fmt_subchunk_id,
            'fmt_subchunk_size': self.fmt_subchunk_size,
            'audio_format': self.audio_format,
            'num_channels': self.num_channels,
            'sample_rate': self.sample_rate,
            'byte_rate': self.byte_rate,
            'block_align': self.block_align,
            'bits_sample': self.bits_sample,
            'data_subchunk_id': self.data_subchunk_id,
            'data_subchunk_size': self.data_subchunk_size,
            'num_frames': self.num_frames,
            'time': self.time,
            'sec_byte': self.sec_byte,
            'sec_sample': self.sec_sample,
            'sec_frame': self.sec_frame,
            'length': self.length
        }
        return {k: v for k, v in params.items() if k not in ignored}

    def set_params(self, params):
        """Multyple params setter

        Arguments:

            params – dict of new params
        """
        for k, v in params.items():
            setattr(self, k, v)

    def read_param(self):
        """Read header and set params

        Fields:

            name – full file name
            content – binary data from file
            length – file size in bytes

            chunk_id – main chunk mark, should be 'RIFF'
            chunk_size – file size without first 8 byte
            chunck_format – format mark, should be 'WAVE'

            fmt_subchunk_id – chunk mark of format
            fmt_subchunk_size – size of chunk format in bytes
            audio_format – compression format
            audio_format_table – tables of compression formats

            num_channels – number of audio channels
            sample_rate – sampling frequency
            byte_rate – byte/sec
                         (sample_rate * frame)
            block_align – frame size in bytes
                           (frame = sample * num_channels)
            bits_sample – size sample quantization in bits

            data_subchunk_id – mark of data chunk
            data_subchunk_size – size of the audio data in bytes

            num_frames – number of frames
            time – duration of audio file
            sec_byte – seconds per byte
            sec_sample – seconds per sample
            sec_frame – seconds per frame
        """
        self.chunk_id = struct.unpack_from('>4s', self.content[0:4])[0]
        self.chunk_size = struct.unpack_from('<L', self.content[4:8])[0]
        self.chunck_format = struct.unpack_from('>4s',
                                                self.content[8:12])[0]

        self.fmt_subchunk_id = struct.unpack_from('>4s',
                                                  self.content[12:16])[0]
        self.fmt_subchunk_size = struct.unpack_from('<l',
                                                    self.content[16:20])[0]

        self.audio_format = struct.unpack_from('<h',
                                               self.content[20:22])[0]

        self.audio_format = self.audio_format_table[self.audio_format]

        self.num_channels = struct.unpack_from('<h',
                                               self.content[22:24])[0]

        self.sample_rate = struct.unpack_from('<l', self.content[24:28])[0]

        self.byte_rate = struct.unpack_from('<l', self.content[28:32])[0]

        self.block_align = struct.unpack_from('<h', self.content[32:34])[0]

        self.bits_sample = struct.unpack_from('<h', self.content[34:36])[0]

        self.data_subchunk_id = struct.unpack_from('>4s',
                                                   self.content[36:40])[0]
        self.data_subchunk_size = struct.unpack_from('<l',
                                                     self.content[40:44])[0]

        self.num_frames = self.data_subchunk_size / self.block_align
        self.time = self.data_subchunk_size / self.byte_rate
        self.sec_byte = self.time / self.data_subchunk_size
        self.sec_sample = self.time / self.num_frames / self.num_channels
        self.sec_frame = self.time / self.num_frames

        self.length = len(self.content)

    def read(self, offset=0):
        """Return data content without header"""
        return list(self.content[500+offset:])
