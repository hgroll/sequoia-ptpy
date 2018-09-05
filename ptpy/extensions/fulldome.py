'''This module extends PTP for Parrot devices.

Use it in a master module that determines the vendor and automatically uses its
extension.
'''
from time import sleep
from datetime import datetime
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
        self.set_device_prop_value('DateTime', str(datetime.now()).encode())

    def StartRecording(self):
        #
        #
        # switch to video mode
        #
        #
        logger.debug(self.SetCameraMode(1))

        # Connect to RTSP
        self.rtsp_init()
        
        # start record mode
        logger.debug(self.SetCameraMode(17))
    
    def StopRecording(self):
        # Disconnect RTSP
        self.rtsp_exit()        

        # Turn Video Off
        logger.debug(self.SetCameraMode(3))


    def StartStopRecording(self, recordingTime):
        self.StartRecording()
        sleep(recordingTime)
        self.StopRecording()

