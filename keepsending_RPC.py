import requests
import time


# 读取IP地址列表
def read_ip_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

    # 发送eth_peerCount请求并获取结果


def get_peer_count(ip, port):
    url = f"http://{ip}:{port}"
    headers = {'Content-Type': 'application/json'}
    payload = '{"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":1}'
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        # 提取并转换peer count
        if 'result' in result and isinstance(result['result'], str):
            peer_count_hex = result['result']
            peer_count = int(peer_count_hex, 16)
            print(f"IP: {ip}, PeerCount: {peer_count}")  # 输出IP和peerCount
            return peer_count
        else:
            print(f"Invalid response from {ip}: {result}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {ip}: {e}")
        return None

    # 主程序


if __name__ == "__main__":
    ip_list_file = 'usual_ip_list.txt'  # 输入文件，包含IP地址
    output_file = 'peer_counts.txt'  # 输出文件，记录peerCount波动范围
    eth_node_port = 8545  # 假设你的Ethereum节点在8545端口上监听
    interval = 1  # 每隔5秒轮询一次
    duration = 24 * 3600  # 总运行时间为5分钟（以秒为单位，24*3600即为24小时）

    ip_list = read_ip_list(ip_list_file)
    peer_counts = {ip: {'min': float('inf'), 'max': -float('inf'), 'last': None} for ip in ip_list}
    start_time = time.time()  # 记录开始时间
    ii=0

    try:
        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time >= duration:  # 如果已过去的时间超过5分钟，则退出循环
                break

            for ip in ip_list:
                peer_count = get_peer_count(ip, eth_node_port)
                if peer_count is not None:
                    peer_counts[ip]['last'] = peer_count
                    peer_counts[ip]['min'] = min(peer_counts[ip]['min'], peer_count)
                    peer_counts[ip]['max'] = max(peer_counts[ip]['max'], peer_count)

                    # 每隔一段时间（比如每次循环结束后）写入当前状态到文件（可选）
            # with open(output_file, 'w') as file:
            #     for ip, stats in peer_counts.items():
            #         file.write(f"{ip}: min={stats['min']}, max={stats['max']}, last={stats['last']}\n")
            ii=ii+1
            time.sleep(interval)  # 等待5秒后再进行下一次循环

    except KeyboardInterrupt:  # 允许使用Ctrl+C中断程序
        pass

        # 脚本结束时，写入最终状态到文件
    with open(output_file, 'w') as file:
        for ip, stats in peer_counts.items():
            file.write(f"{ip}: min={stats['min']}, max={stats['max']}, last={stats['last']}\n")

    print("Script finished. Results saved to", output_file)
    print("遍历次数：",ii)