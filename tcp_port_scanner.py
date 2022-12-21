import optparse
from socket import *
from threading import *

screenLock = Semaphore(value = 1)

def connScan(targetHost, targetPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((targetHost, targetPort))
        connSkt.send(b'send test\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print('[O]%d' % targetPort)
        # print('[C] ' + str(results))
    except:
        screenLock.acquire()
        print('[C]%d' % targetPort)
    finally:
        screenLock.release()
        connSkt.close()

def portScan(targetHost, targetPorts):
    try:
        targetIP = gethostbyname(targetHost)
    except:
        print("Cannot resolve '%s': unknown host" % targetHost)
        return
    try:
        targetName = gethostbyaddr(targetIP)
        print('Results[%s]:' % targetName[0])
    except:
        print('Results[%s]:' % targetIP)
    setdefaulttimeout(1)
    for targetPort in targetPorts:
        t = Thread(target=connScan, args=(targetHost, int(targetPort)))
        t.start()
    
def main():
    parser = optparse.OptionParser('usage % prog -H <target host> -P <target port>')
    parser.add_option('-H', dest='targetHost', type='string', help='specify target host')
    parser.add_option('-p', dest='targetPort', type='string', help='specify target[s] separated by comma')

    [options, args] = parser.parse_args()
    targetHost = options.targetHost
    targetPorts = str(options.targetPort).split(',')
    if (targetHost == None) | (targetPorts[0] == None):
        print(parser.usage)
        exit(0)
    portScan(targetHost, targetPorts)

if __name__ == "__main__":
    main()