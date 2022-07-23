from common.logging import InfoLogger, InfoLogger, ErrorLogger

from copy import deepcopy

class TCP:

    @staticmethod
    def send(conn, msg):
        try:
            msg = deepcopy(msg)

            msg_encode, res = TCP.encode(msg)
            if res: return res

            header, res = TCP.encode(len(msg_encode))
            if res: return res
            conn.send(header)

            ack = conn.recv(32)
            conn.send(msg_encode)

        except Exception as e:
            ErrorLogger.error(f'tcp.send.fail. Details {str({"msg": msg, "error": e})}')
            return e

        InfoLogger.info(f'tcp.send.success. Details {str({"msg": msg, "header": header, "payload": msg_encode})}')
        return None

    @staticmethod
    def recv(conn):
        try:
            msg = conn.recv(32)
            msg_decode, res = TCP.decode(msg)
            if res:
                ErrorLogger.error(f'tcp.recv.fail.')
                return None, res

            size = int(msg_decode)

            ack = bytes(str("ACK"), 'utf8')
            conn.send(ack)

            msg = conn.recv(size)
            msg_decode, res = TCP.decode(msg)
            if res:
                ErrorLogger.error(f'tcp.recv.fail.')
                return None, res
            if msg_decode == 'CLOSE':
                InfoLogger.info(f'tcp.recv.close.')
                return "CLOSE", None

        except Exception as e:
            ErrorLogger.error(f'tcp.recv.fail. Details {str({"error": e})}')
            return e

        InfoLogger.info(f'tcp.recv.success. Details {str({"msg": msg_decode})}')
        return msg_decode, None

    @staticmethod
    def close(conn):
        try:
            msg = "CLOSE"
            res = TCP.send(conn, msg)
            if res:
                ErrorLogger.error(f'tcp.close.fail.')
                return res

        except Exception as e:
            ErrorLogger.error(f'tcp.close.fail. Details {str({"error": e})}')
            return e

        InfoLogger.info(f'tcp.close.success.')
        return None

    @staticmethod
    def encode(msg):
        try:
            if type(msg) is str:
                InfoLogger.info(f'tcp.encode.success. Details: {str({"msg": msg})}')
                return bytes(msg, 'utf8'), None

            elif type(msg) in [int, bool, float]:
                msg_encode, res = TCP.encode(str(msg))
                if res:
                    ErrorLogger.error(f'tcp.encode.fail.')
                    return None, res

                InfoLogger.info(f'tcp.encode.success. Details: {str({"msg": msg})}')
                return msg_encode, None

            elif type(msg) is list:
                msg_bytes = []
                for i, m in enumerate(msg):
                    msg_byte, res = TCP.encode(m)
                    if res:
                        ErrorLogger.error(f'tcp.encode.fail.')
                        return None, res
                    msg_bytes += [msg_byte]

                InfoLogger.info(f'tcp.encode.success. Details: {str({"msg": msg})}')
                return bytes(str(msg_bytes), 'utf8'), None

            elif type(msg) is dict:
                for key, val in msg.items():
                    msg[key], res = TCP.encode(val)
                    if res:
                        ErrorLogger.error(f'tcp.encode.fail.')
                        return None, res

                InfoLogger.info(f'tcp.encode.success. Details: {str({"msg": msg})}')
                return bytes(str(msg), 'utf8'), None

            elif msg is None:
                return bytes('', 'utf8'), None

        except Exception as e:
            ErrorLogger.error(f'tcp.encode.fail. Details {str({"msg": msg, "error": e})}')
            return None, e

        ErrorLogger.error(f'tcp.encode.message_type_not_supported. Details {str({"type": type(msg)})}')
        return Exception('tcp.encode.message_type_not_supported')


    @staticmethod
    def decode(msg):
        try:
            msg_str = msg.decode('utf8')
        except Exception as e:
            ErrorLogger.error(f'tcp.decode.fail. Details {str({"msg": msg, "error": e})}')
            return None, e

        # in case input is purely string, eval will throw Exception, then return it without evaluating
        try:
            msg_object = eval(msg_str)
        except:
            InfoLogger.info(f'tcp.decode.success. Details {str({"msg": msg_str})}')
            return msg_str, None

        try:
            if type(msg_object) is list:
                for i, m in enumerate(msg_object):
                    msg_object[i], res = TCP.decode(m)
                    if res:
                        ErrorLogger.error(f'tcp.decode.fail.')
                        return None, res

                InfoLogger.info(f'tcp.decode.success. Details {str({"msg": msg_str, "msg_object": msg_object})}')
                return msg_object, None

            elif type(msg_object) is dict:
                for key, val in msg_object.items():
                    msg_object[key], res = TCP.decode(val)
                    if res:
                        ErrorLogger.error(f'tcp.decode.fail.')
                        return None, res

                InfoLogger.info(f'tcp.decode.success. Details {str({"msg": msg_str, "msg_object": msg_object})}')
                return msg_object, None

            elif type(msg_object) in [int, bool, float]:
                InfoLogger.info(f'tcp.decode.success. Details {str({"msg": msg_str, "msg_object": msg_object})}')
                return msg_object, None

        except Exception as e:
            ErrorLogger.error(f'tcp.decode.fail. Details {str({"msg": msg, "error": e})}')
            return None, e

        ErrorLogger.error(f'tcp.decode.message_type_not_supported. Details {str({"type": type(msg)})}')
        return None, Exception('tcp.decode.message_type_not_supported')
