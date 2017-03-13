#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Lucky lau
# E-mail:laujunbupt0913@163com
#
# apt-get install python-pycurl

"""
    {
      "description": "",
      "enable_dhcp": true,
      "network_id": "941983b2-d327-4c0c-80b5-807805acc7ec",
      "tenant_id": "8a80a65d5a8cf61a015ab26541a6639a",
      "created_at": "2017-03-10T13:15:04",
      "dns_nameservers": [
        "10.0.100.166"
      ],
      "updated_at": "2017-03-10T13:15:04",
      "gateway_ip": "7.7.7.1",
      "ipv6_ra_mode": null,
      "allocation_pools": [
        {
          "start": "7.7.7.2",
          "end": "7.7.7.254"
        }
      ],
      "host_routes": [],
      "ip_version": 4,
      "ipv6_address_mode": null,
      "cidr": "7.7.7.0/24",
      "id": "4cf76f7f-4129-4b95-a29b-45551823b590",
      "subnetpool_id": null,
      "name": "loab3-subnet"
    }
"""

import pycurl
import json
import time
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


def url_invoke(url, request_json):

    header1 = "Accept: application/json"
    header2 = "Accept-Encoding: gzip, deflate"
    header3 = "X_ROLES: admin"
    header4 = "X_USER_ID: 9527"
    header5 = "X_PROJECT_ID: admin"
    header = [header1, header2, header3, header4, header5]

    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, str(url))
    curl.setopt(curl.CONNECTTIMEOUT, 30)
    curl.setopt(curl.TIMEOUT, 10)
    curl.setopt(curl.HTTPHEADER, header)
    if request_json:
        curl.setopt(curl.POSTFIELDS, json.dumps(request_json))
    curl.setopt(curl.WRITEFUNCTION, buffer.write)
    try:
        curl.perform()
    except pycurl.error as e:
        curl.close()
        return None

    res = json.loads(buffer.getvalue())
    print res


def set_url(host, interface, resoure_id):
    if resoure_id:
        url = "http://%s:9696/v2.0/%s/%s" % (host, interface, resoure_id)
        return url
    url = "http://%s:9696/v2.0/%s" % (host, interface)
    return url


if __name__ == '__main__':
    # eg: get subnet
    url = set_url(
        "10.0.38.110",
        "subnets",
        "4cf76f7f-4129-4b95-a29b-45551823b590")
    url_invoke(url, None)
    # eg : post subnet
    request_json = {
        "subnet": {
            "network_id": "941983b2-d327-4c0c-80b5-807805acc7ec",
            "ip_version": 4,
            "cidr": "12.12.12.0/24"
        }
    }
    url=set_url("10.0.38.110",
        "subnets",None)
    url_invoke(url, request_json)
