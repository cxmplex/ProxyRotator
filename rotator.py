import re
from os.path import abspath
from itertools import cycle


class Rotator:
    proxies = {"file": [], "retries": [], "banned": []}
    pools = {}

    def __init__(self, proxy_list: str):
        print("Initializing proxy rotator")
        self._read_proxies(proxy_list)
        if not len(self.proxies["file"]) > 0:
            print("Failed to init proxies")
        self._init_cycling()

    def _read_proxies(self, proxy_list):
        with open(abspath(proxy_list)) as f:
            re_ip_addr = re.compile(r"((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
                                    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(:\d{2,5})")
            for line in f:
                m = re.match(re_ip_addr, line)
                if m is not None:
                    self.proxies["file"].append((m.group(1), m.group(2)))
        print("{} proxies loaded".format(len(self.proxies["file"])))

    def _init_cycling(self):
        self.pools["running"] = cycle(self.proxies["file"])
        self.pools["retries"] = cycle(self.proxies["retries"])

    def ban_proxy(self, proxy):
        self.proxies["running"].remove(proxy)
        self.proxies["banned"].append(proxy)

    def _get_proxy_statistics(self):
        print("Running: {}, Banned: {}, Valid %: {}".format(len(self.proxies["running"]), len(self.proxies["banned"]),
                                                            len(self.proxies["banned"])/len(self.proxies["running"])))

    def get_proxy(self):
        return next(self.pools["running"])

    def get_retry(self):
        return next(self.pools["retries"])
    
    def add_retry(self, proxy):
        self.proxies["running"].remove(proxy)
        self.proxies["retries"].append(proxy)

