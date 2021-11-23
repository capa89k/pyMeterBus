# -*- coding: utf-8 -*-

"""upython meterbus

    A library to decode M-Bus frames on upython devices.

    :copyright: (c) 2017-2021 by Mikael Ganehag Brorsson.
    :license: BSD, see LICENSE for more details.
"""

from meterbus.defines import *

from meterbus.core_objects import (
    DataEncoding,
    FunctionType,
    MeasureUnit,
    VIFUnit,
    VIFUnitExt,
    VIFUnitSecExt,
    VIFTable,
    DateCalculator)

from meterbus.telegram_ack import TelegramACK
from meterbus.telegram_short import TelegramShort
from meterbus.telegram_control import TelegramControl
from meterbus.telegram_long import TelegramLong

from meterbus.data_information_block import DataInformationBlock
from meterbus.value_information_block import ValueInformationBlock
from meterbus.telegram_header import TelegramHeader
from meterbus.telegram_body import (
    TelegramBody,
    TelegramBodyHeader,
    TelegramBodyPayload)
from meterbus.telegram_field import TelegramField
from meterbus.telegram_variable_data_record import TelegramVariableDataRecord

from meterbus.wtelegram_snd_nr import WTelegramSndNr
from meterbus.wtelegram_body import WTelegramFrame
from meterbus.wtelegram_header import WTelegramHeader

from meterbus.exceptions import MBusFrameDecodeError, FrameMismatch

from meterbus.serial import *
from meterbus.auxiliary import *

__author__ = "Mikael Ganehag Brorsson"
__license__ = "BSD-3-Clause"
__version__ = "0.8.1"


def load(data):
    if not data:
        raise MBusFrameDecodeError("empty frame", data)

    if isinstance(data, str):
        data = list(map(ord, data))

    elif isinstance(data, bytes):
        data = list(data)

    elif isinstance(data, bytearray):
        data = list(data)

    elif isinstance(data, list):
        pass

    for Frame in [WTelegramSndNr, TelegramACK, TelegramShort, TelegramControl,
                  TelegramLong]:
        try:
            return Frame.parse(data)

        except FrameMismatch:
            pass

    raise MBusFrameDecodeError("unable to decode frame")
