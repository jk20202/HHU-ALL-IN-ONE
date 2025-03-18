from mitmproxy import http
import json
from mitmproxy.tools.main import mitmdump, mitmweb
import sys
import argparse
from loguru import logger


def response(flow: http.HTTPFlow) -> None:
    if "searchByDate" in flow.request.url:
        logger.info('exam')
        data = json.loads(flow.response.text)
        logger.info(data)
        data_list = data['data']['list']
        for i in range(len(data_list)):
            slotInfo = data_list[i]['slotInfo']
            for j in range(len(slotInfo)):
                slotInfo[j]['status'] = 0
            data_list[i]['status'] = 0
        flow.response.text = json.dumps(data, ensure_ascii=False)



if __name__ == "__main__":
    # 记得windows代理设置
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-P", "--port", type=int, default=8888, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]
    mitmdump()

    # sys.argv = ["mitmweb", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]
    # mitmweb()