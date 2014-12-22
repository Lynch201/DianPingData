import base64
import random
# Start your middleware class
global num
num = 0

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        i = random.randint(0, len(self.proxyList) - 1)

        request.meta['proxy'] = self.proxyList[i]

        print "-------------" + str( request.meta['proxy'])
        # Use the following lines if your proxy requires authentication
        proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

    proxyList = [
        "http://119.6.144.70:843",
        "http://119.6.144.78:80",
        "http://218.108.170.166:82",
        "http://61.156.3.166:80",

        ]


class ProxyGoAgent(object):
    def process_request(self, request, spider):

        print "-----http://127.0.0.1:8087"
        request.meta['proxy'] = "http://test.theqingyun.co:16275"
        proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass


