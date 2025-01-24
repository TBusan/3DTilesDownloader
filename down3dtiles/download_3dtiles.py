import os
import json
import requests
from pathlib import Path
import time

class TilesDownloader:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'origin': 'http://mars3d.cn',
            'host': 'data1.mars3d.cn',
            'accept-encoding': 'gzip, deflate',
            'referer': 'http://mars3d.cn/'
        }
        self.downloaded_files = set()
        
    def download_file(self, url, save_path, parent_folder=None):
        """
        下载文件并保存到指定路径
        :param url: 文件的相对URL
        :param save_path: 保存路径
        :param parent_folder: json文件所在的父文件夹名
        """
        if save_path in self.downloaded_files:
            print(f"已下载: {save_path}")
            return True
            
        try:
            # 构建完整的URL
            if parent_folder:
                # 对于在Data目录下的文件，需要考虑父文件夹路径
                full_url = f"{self.base_url}/Data/{parent_folder}/{url}"
            elif url.startswith('Data/'):
                # 对于完整路径的文件
                full_url = f"{self.base_url}/{url}"
            else:
                # 其他文件直接拼接
                full_url = f"{self.base_url}/{url}"
            
            print(f"正在下载: {full_url}")
            
            # 添加重试机制
            max_retries = 3
            for retry in range(max_retries):
                try:
                    response = requests.get(full_url, headers=self.headers)
                    response.raise_for_status()
                    break
                except requests.RequestException as e:
                    if retry == max_retries - 1:
                        raise e
                    print(f"重试 {retry + 1}/{max_retries}: {url}")
                    time.sleep(1)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 保存文件
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            self.downloaded_files.add(save_path)
            print(f"下载完成: {save_path}")
            
            # 如果是json文件，解析并下载其中引用的文件
            if url.endswith('.json'):
                self.process_json_file(save_path)
                
            return True
            
        except Exception as e:
            print(f"下载失败 {url}: {str(e)}")
            return False

    def process_json_file(self, json_path):
        """处理json文件，提取并下载其中引用的文件"""
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            # 获取json文件所在的父文件夹名
            parent_folder = os.path.basename(os.path.dirname(json_path))
            
            # 递归处理所有节点
            self.extract_urls_from_node(data.get('root', {}), os.path.dirname(json_path), parent_folder)
            
        except Exception as e:
            print(f"处理JSON文件失败 {json_path}: {str(e)}")

    def extract_urls_from_node(self, node, base_path, parent_folder):
        """从节点中提取URL并下载相关文件"""
        if 'content' in node and 'url' in node['content']:
            url = node['content']['url']
            
            # 处理文件路径
            if url.endswith('.json'):
                # 从url中提取Tile_xxx部分作为文件夹名
                tile_folder = url.split('/')[1] if '/' in url else parent_folder
                # json文件保存在Data/Tile_xxx/目录下
                folder_path = os.path.join(self.output_dir, 'Data', tile_folder)
                local_path = os.path.join(folder_path, os.path.basename(url))
            else:
                # b3dm文件保存在当前json文件所在目录
                local_path = os.path.join(base_path, url)
            
            # 下载文件
            self.download_file(url, local_path, parent_folder)

        # 递归处理children节点
        if 'children' in node:
            for child in node['children']:
                self.extract_urls_from_node(child, base_path, parent_folder)

    def process_tileset(self, tileset_path, base_path):
        """处理本地的tileset.json文件并下载所有相关文件"""
        self.output_dir = base_path
        
        try:
            # 读取本地的tileset.json
            with open(tileset_path, 'r') as f:
                data = json.load(f)
            
            # 将tileset.json复制到输出目录
            output_tileset = os.path.join(base_path, 'tileset.json')
            os.makedirs(base_path, exist_ok=True)
            with open(output_tileset, 'w') as f:
                json.dump(data, f)
            
            # 递归处理所有节点
            self.extract_urls_from_node(data.get('root', {}), base_path, '')
            
        except Exception as e:
            print(f"处理tileset.json失败: {str(e)}")

def main():
    # 基础URL
    base_url = "http://data1.mars3d.cn/3dtiles/qx-simiao"
    
    # 创建下载目录
    output_dir = "downloaded_tiles"
    
    # 使用本地的tileset.json
    tileset_path = "tileset.json"
    
    # 创建下载器实例并开始下载
    try:
        downloader = TilesDownloader(base_url)
        print("开始下载...")
        downloader.process_tileset(tileset_path, output_dir)
        print("\n下载完成!")
        
    except Exception as e:
        print(f"\n下载出错: {str(e)}")
        print("下载失败!")

if __name__ == "__main__":
    main() 