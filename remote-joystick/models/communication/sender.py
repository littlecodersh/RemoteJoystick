from jssocket import jssocket

class sender(object):
    __client = jssocket()
    __connected = False
    def __init__(self):
        pass
    def connect(self, serverInfo, verifyCode):
        if self.__connected == True: return True
        self.__client.connect(serverInfo)
        self.__client.push(1, ('0000' + verifyCode)[-4:])
        msgType, msgData = self.__client.pull()
        if msgType == 1 and msgData == verifyCode:
            self.__connected = True
            return True
        else:
            self.__client.push(0, b'\x00\x00\x00\x00')
            self.__client.close()
            return False
    def disconnect(self):
        if self.__connected == False: return
        self.__client.push(0, b'\x00\x00\x00\x00')
        self.__client.close()
        self.__connected = False
    def sendMsg(self, data):
        if not self.__connected: return False
        self.__client.push(3, (b'\x00\x00\x00\x00' +
            data)[-4:])
        return True

if __name__ == '__main__':
    s = sender()
    while not s.connect(('120.27.119.189', 2333), '1234'): pass
    print('Connected')
    try:
        while s.sendMsg(raw_input('>')): pass
    except KeyboardInterrupt:
        s.disconnect()