'''This module extends PTP for Parrot devices.

Use it in a master module that determines the vendor and automatically uses its
extension.
'''
from time import time, sleep
import socket
from ptpy.transports.ip import create_connection, actual_socket
from construct import (
    Container, Enum, ExprAdapter, Pass, Struct,
)
import logging
logger = logging.getLogger(__name__)

__all__ = ('fulldome',)


class Fulldome(object):
    '''This class implements Fulldome's PTP operations.'''

    def __init__(self, *args, **kwargs):
        logger.debug('Init Fulldome')
        super(Fulldome, self).__init__(*args, **kwargs)

    def rtsp_init(self):
        # RTSP Connection Establishment
        self.__rtspcon = create_connection(('192.168.1.1', 554))
        self.__rtspcon.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.__rtspcon.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        describe_string = ("DESCRIBE rtsp://192.168.1.1:554/H264?W=1920&H=960&BR=3000000&FPS=30 RTSP/1.0\r\n CSeq: 2\r\n" +
                           "User-Agent: ICatchMedia (LIVE555 Streaming Media v2013.06.06)\r\n" +
                           "Accept: application/sdp\r\n" +
                           "\r\n")
        actual_socket(self.__rtspcon).sendall(str.encode(describe_string))
        response = actual_socket(self.__rtspcon).recv(1024)
        logger.debug(response)

    def rtsp_exit(self):
        logger.debug('rtsp_exit')

        try:
            self.__rtspcon.shutdown(socket.SHUT_RDWR)
        except socket.error as e:
            if e.errno == 107:
                pass
            else:
                raise e
        self.__rtspcon.close()


    def _PropertyCode(self, **product_properties):
        return super(Fulldome, self)._PropertyCode(
            CameraMode=0xD604,
            VideoResolution=0xD605,
            RecordProperty1=0xD610,
            RecordProperty3=0xD7F2,
            **product_properties
        )

    def _OperationCode(self, **product_operations):
        return super(Fulldome, self)._OperationCode(
            UnknownCommand=0x9601,
            **product_operations
        )

    def _ResponseCode(self, **product_responses):
        return super(Fulldome, self)._ResponseCode(
            **product_responses
        )

    def _EventCode(self, **product_events):
        return super(Fulldome, self)._EventCode(
            **product_events
        )
    def SetCameraMode(self, mode):
        code = self._PropertyCode.encoding['CameraMode']
        ptp = Container(
            OperationCode='SetDevicePropValue',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[code],
        )
        payload = self._UInt16.build(mode)
        response = self.send(ptp, payload)
        return response
    def SendUnknownCommand(self):
        '''Send Unknown Command'''
        ptp = Container(
            OperationCode='UnknownCommand',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[0xd001, 0xffffffff, 0x00000000],
        )
        return self.mesg(ptp)
    def SyncTime(self):
        '''Sync Time with Host'''
        self.set_device_prop_value('DateTime', datetime.now())

    def StartRecording(self):
        logger.debug(self.get_device_info())
        logger.debug(self.get_object_handles(0, all_storage_ids=True, in_root=True))
        logger.debug(self.get_storage_ids())
        logger.debug(self.get_object_handles(0x00020001, in_root=True))
        logger.debug(self.get_device_prop_desc('CameraMode'))
        logger.debug(self.get_device_prop_value('CameraMode'))
        sleep(1)
        # get device info
        logger.debug(self.get_device_info())
        logger.debug(self.get_device_prop_desc(0xd7fe))
        sleep(1)
        logger.debug(self.SendUnknownCommand())
        sleep(1)
        logger.debug(self.get_device_prop_desc(0xd7ab))
        sleep(1)
        logger.debug(self.get_device_prop_desc(0xd7ab))
        sleep(1)
        logger.debug(self.get_device_prop_desc(0xd7ae))
        sleep(1)
        logger.debug(self.get_device_prop_desc('WhiteBalance'))
        sleep(1)
        logger.debug(self.get_device_prop_desc('VideoResolution'))
        sleep(1)
        logger.debug(self.get_device_prop_desc('ImageSize'))
        sleep(1)
        logger.debug(self.get_device_prop_desc(0xd607))
        sleep(1)
        logger.debug(self.get_device_prop_value('Artist'))
        sleep(1)
        # GetDate
        # SetDate
        logger.debug(self.get_device_prop_desc(0xd801))
        sleep(1)
        logger.debug(self.get_device_prop_desc('RecordProperty1'))
        logger.debug(self.get_device_prop_value('RecordProperty1'))
        sleep(1)
        logger.debug(self.get_device_prop_desc(0xd7ab))
        sleep(1)
        logger.debug(self.SetCameraMode(3))
        sleep(1)
        logger.debug(self.SendUnknownCommand())
        sleep(1)
        logger.debug(self.get_device_prop_value('ImageSize'))
        sleep(1)
        # GetStorageIDs
        logger.debug(self.get_storage_ids())
        logger.debug(self.get_storage_info(0x00020001))
        logger.debug(self.get_storage_info(0x00020001))
        logger.debug(self.get_device_prop_desc('BatteryLevel'))
        logger.debug(self.get_device_prop_value('BatteryLevel'))
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        #
        #
        # switch to video mode
        #
        #
        logger.debug(self.get_storage_info(0x00020001))
        logger.debug(self.get_device_prop_desc('RecordProperty3'))
        logger.debug(self.get_device_prop_desc(0xd7ab))
        logger.debug(self.SetCameraMode(1))
        sleep(1)
        logger.debug(self.SendUnknownCommand())
        sleep(1)
        logger.debug(self.get_device_prop_value('VideoResolution'))
        logger.debug(self.get_device_prop_desc('RecordProperty1'))
        logger.debug(self.get_device_prop_value('RecordProperty1'))
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)

        # Connect to RTSP
        self.rtsp_init()
        
        # Video Aufnahme
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.get_device_prop_desc('RecordProperty1'))
        logger.debug(self.get_device_prop_value('RecordProperty1'))
        logger.debug(self.get_device_prop_value('VideoResolution'))
        logger.debug(self.get_device_prop_desc('RecordProperty3'))
        logger.debug(self.SetCameraMode(17))
        logger.debug(self.SendUnknownCommand())
        sleep(1)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)

        # Disconnect RTSP
        self.rtsp_exit()        

        # Turn Video Off
        logger.debug(self.SetCameraMode(3))

    def StartRecordingSimple(self):
        #
        #
        # switch to video mode
        #
        #
        logger.debug(self.SetCameraMode(1))
        sleep(1)

        #logger.debug(self.SendUnknownCommand())
        #sleep(1.5)

        # Connect to RTSP
        self.rtsp_init()
        
        # Video Aufnahme
        logger.debug(self.SetCameraMode(17))
        logger.debug(self.SendUnknownCommand())
        sleep(1)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)
        logger.debug(self.SendUnknownCommand())
        sleep(1.5)

        # Disconnect RTSP
        self.rtsp_exit()        

        # Turn Video Off
        logger.debug(self.SetCameraMode(3))

    
