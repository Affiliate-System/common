from common.error import *
from common.logging import InfoLogger, InfoLogger, ErrorLogger

from copy import deepcopy

class TCP:

    @staticmethod
    def send(conn, msg):
        msg = deepcopy(msg)
        try:
            msg_encode, res = TCP.encode(msg)
            if res: return res

            header, res = TCP.encode(len(msg_encode))
            if res: return res
            conn.send(header)
            InfoLogger.info(f"Send tcp header {header}")

            ack = conn.recv(32)
            conn.send(msg_encode)
            InfoLogger.info(f"Send tcp payload {msg_encode}")
        except Exception as e:
            err = TcpSocketError(e)
            ErrorLogger.error(str(err))
            return err

        return None

    @staticmethod
    def recv(conn):
        try:
            msg = conn.recv(32)
            msg_decode, res = TCP.decode(msg)
            InfoLogger.info(f"Message decoded {msg_decode}")
            if res: return None, res

            size = int(msg_decode)
            InfoLogger.info(f"Tcp payload size to receive {size}")

            ack = bytes(str("ACK"), 'utf8')
            conn.send(ack)

            msg = conn.recv(size)
            msg_decode, res = TCP.decode(msg)
            InfoLogger.info(f"Receive tcp payload {msg_decode}")
            if res: return None, res
            if msg_decode == 'CLOSE':
                return "CLOSE", None

        except Exception as e:
            err = TcpSocketError(e)
            ErrorLogger.error(str(err))
            return None, err

        return msg_decode, None

    @staticmethod
    def close(conn):
        try:
            msg = "CLOSE"
            res = TCP.send(conn, msg)
            if res: return res
        except Exception as e:
            err = TcpSocketError(e)
            ErrorLogger.error(str(err))
            return err

        return None

    @staticmethod
    def encode(msg):
        InfoLogger.info(f"Message to encode: {msg}")
        try:
            if type(msg) is str:
                return bytes(msg, 'utf8'), None

            elif type(msg) in [int, bool, float]:
                msg_encode, res = TCP.encode(str(msg))
                if res: return None, res
                return msg_encode, None

            elif type(msg) is list:
                msg_bytes = []
                for i, m in enumerate(msg):
                    msg_byte, res = TCP.encode(m)
                    if res: return None, res
                    msg_bytes += [msg_byte]
                return bytes(str(msg_bytes), 'utf8'), None

            elif type(msg) is dict:
                for key, val in msg.items():
                    msg[key], res = TCP.encode(val)
                    if res: return None, res
                return bytes(str(msg), 'utf8'), None

            elif msg is None:
                return bytes('', 'utf8'), None

            err = TcpSocketError(f"Cannot encode type {type(msg)}")
            ErrorLogger.error(str(err))
            return None, err

        except Exception as e:
            err = TcpSocketError(str(e))
            ErrorLogger.error(str(err))
            return None, err

    @staticmethod
    def decode(msg):
        InfoLogger.info(f"Message to decode: {msg}")
        try:
            msg_str = msg.decode('utf8')
        except Exception as e:
            err = TcpSocketError(str(e))
            ErrorLogger.error(str(err))
            return None, err

        # in case input is purely string, return it without evaluating
        try:
            InfoLogger.info(f"Decode from message {msg} to string message {msg_str}")
            msg_object = eval(msg_str)
        except:
            return msg_str, None

        try:
            if type(msg_object) is list:
                for i, m in enumerate(msg_object):
                    msg_object[i], res = TCP.decode(m)
                    if res: return None, res
                return msg_object, None

            elif type(msg_object) is dict:
                for key, val in msg_object.items():
                    msg_object[key], res = TCP.decode(val)
                    if res: return None, res
                return msg_object, None

            elif type(msg_object) in [int, bool, float]:
                return msg_object, None

            err = TcpSocketError(f"Cannot decode type {type(msg_object)}")
            ErrorLogger.error(str(err))
            return None, err

        except Exception as e:
            err = TcpSocketError(str(e))
            ErrorLogger.error(str(err))
            return None, err
