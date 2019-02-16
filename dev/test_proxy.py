from bs4 import BeautifulSoup
import urllib2
import httplib
import threading
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

inFile = open('proxy.txt', 'a+')
outFile = open('verified.txt', 'a+')
lock = threading.Lock()

proxyFile = open('proxy.txt', 'a+')


def getProxyList(targeturl="http://www.xicidaili.com/nn/"):
    countNum = 0

    requestHeader = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}

    for page in range(1, 10):
        url = targeturl + str(page)
        # print url

?  # urllib2����headers��Ϣ
request = urllib2.Request(url, headers=requestHeader)
html_doc = urllib2.urlopen(request).read()
?  # bs4Ԫ�ز���
soup = BeautifulSoup(html_doc, "html.parser")
# print soup
trs = soup.find('table', id='ip_list').find_all('tr')
for tr in trs[1:]:
    # print tr
    tds = tr.find_all('td')
    # ����Cn
    if tds[0].find('img') is None:
        nation = 'δ֪'
        locate = 'δ֪'
    else:
        nation = tds[0].find('img')['alt'].strip()
        locate = tds[3].text.strip()
    ip = tds[1].text.strip()  # ip
    # print 'ip:',ip
    port = tds[2].text.strip()  # �˿�
    anony = tds[5].text.strip()
    protocol = tds[6].text.strip()
    speed = tds[7].find('div')['title'].strip()
    time = tds[9].text.strip()
    with open('proxy.txt', 'a+') as proxyFile:
        proxyFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol, speed, time))
    # print '%s=%s:%s' % (protocol, ip, port)
    countNum += 1

# proxyFile.close()
return countNum


def verifyProxyList():
    '''
    ��֤�������Ч��
    '''
    requestHeader = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    myurl = 'http://www.baidu.com/'

    while True:
        lock.acquire()
        ll = proxyFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split('|')
        # protocol = line[5]
        ip = line[1]
        port = line[2]
        print(ll)

        try:
            conn = httplib.HTTPConnection(ip, port, timeout=5.0)
            conn.request(method='GET', url=myurl, headers=requestHeader)
            res = conn.getresponse()
            lock.acquire()
            print("+++Success:" + ip + ":" + port)
            outFile.write(ll + "\n")
            lock.release()
        except:
            print("---Failure:" + ip + ":" + port)


if __name__ == '__main__':
    tmp = open('proxy.txt', 'w')
    tmp.write("")
    tmp.close()
    proxynum = getProxyList("http://www.xicidaili.com/nn/")
    print("���ڸ��䣺" + str(proxynum))
    proxynum = getProxyList("http://www.xicidaili.com/nt/")
    print("����͸����" + str(proxynum))
    proxynum = getProxyList("http://www.xicidaili.com/wn/")
    print("������䣺" + str(proxynum))
    proxynum = getProxyList("http://www.xicidaili.com/wt/")
    print("����͸����" + str(proxynum))

    print("\n��֤�������Ч�ԣ�")

    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()

    inFile.close()
    outFile.close()

---------------------
���ߣ�Eric - ׷��
��Դ��CSDN
ԭ�ģ�https: // blog.csdn.net / zhiaicq_r / article / details / 79273915
��Ȩ����������Ϊ����ԭ�����£�ת���븽�ϲ������ӣ�