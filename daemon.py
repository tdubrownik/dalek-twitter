import socket, time, urllib, urllib2, random, json, struct
from datetime import datetime

def get_datetime(tweet):
    return datetime.strptime(tweet['created_at'][:-6],
        '%a, %d %b %Y %H:%M:%S')

class DalekTwitter(object):
    api_url = 'http://search.twitter.com/search.json'
    def __init__(self, options, *a, **kw):
        self.options = options
        self.last_tid = self.read_last_tid()
        self.ua = 'adenozynotrojfosforan'
    def read_last_tid(self):
        try:
            with open(self.options.last_id_file, 'r') as f:
                return int(f.readline())
        except (ValueError, IOError):
            return 0
    def write_last_tid(self, tid):
        if tid:
            with open(self.options.last_id_file, 'w') as f:
                f.write(str(tid))
    def rua(self):
        l = list(self.ua)
        random.shuffle(l)
        self.ua = ''.join(l)
    def poll_twitter(self):
        args = urllib.urlencode({
            'q': self.options.twitter_query,
            'since_id': self.last_tid
        })
        self.rua()
        req = urllib2.Request(self.api_url + '?' + args, None,
            { 'User-Agent': self.ua })
        r = urllib2.urlopen(req)
        return json.load(r)
    def dalek_write(self, m):
        um = m.encode('utf-8')
        s = socket.socket()
        s.connect((self.options.host, self.options.port))
        s.send('m' + struct.pack('!I', len(um)) + um)
    def format_tweet(self, tweet):
        return '\n%s %s: %s\n' % \
            (get_datetime(tweet).strftime('%d/%m/%y %H:%M'), 
                tweet['from_user'], tweet['text'])
    def start(self):
        try:
            while True:
                print 'refreshing'
                reply = self.poll_twitter()
                self.last_tid = reply['max_id']
                print 'last id:', self.last_tid
                self.write_last_tid(self.last_tid)
                for tweet in reply['results']:
                    will_write = self.format_tweet(tweet)
                    print 'Will send:\n', will_write
                    self.dalek_write(will_write)
                time.sleep(self.options.twitter_refresh)
        except KeyboardInterrupt:
            self.write_last_tid(self.last_tid)

if __name__ == '__main__':
    import options
    DalekTwitter(options).start()
