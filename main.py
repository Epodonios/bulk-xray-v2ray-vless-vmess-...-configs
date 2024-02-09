import requests
from bs4 import BeautifulSoup
import os
import shutil
from datetime import datetime
import urllib.parse


def get_v2ray_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        divs = soup.find_all('div', class_='tgme_widget_message_text')
        divs2 = soup.find_all('div', class_='tgme_widget_message_text js-message_text before_footer')
        spans = soup.find_all('span', class_='tgme_widget_message_text')
        codes = soup.find_all('code')
        span = soup.find_all('span')
        main = soup.find_all('div')
        
        all_tags = divs + spans + codes + divs2 + span + main

        v2ray_configs = []
        for tag in all_tags:
            text = tag.get_text()
            if text.startswith('vless://') or text.startswith('ss://') or text.startswith('trojan://') or text.startswith('tuic://'):
                v2ray_configs.append(text)

        return v2ray_configs
    else:
        print(f"Failed to fetch URL (Status Code: {response.status_code})")
        return None

def get_region_from_ip(ip):
    api_endpoints = [
        f'https://ipapi.co/{ip}/json/',
        f'https://ipwhois.app/json/{ip}',
        f'http://www.geoplugin.net/json.gp?ip={ip}',
        f'https://api.ipbase.com/v1/json/{ip}'
    ]

    for endpoint in api_endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                if 'country' in data:
                    return data['country']
        except Exception as e:
            print(f"Error retrieving region from {endpoint}: {e}")
    return None

def save_configs_by_region(configs):
    config_folder = "sub"
    if os.path.exists(config_folder):
        for folder in os.listdir(config_folder):
            folder_path = os.path.join(config_folder, folder)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)

    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    for config in configs:
        ip = config.split('//')[1].split('/')[0]
        region = get_region_from_ip(ip)
        if region:
            region_folder = os.path.join(config_folder, region)
            if not os.path.exists(region_folder):
                os.makedirs(region_folder)

            with open(os.path.join(region_folder, 'config.txt'), 'a', encoding='utf-8') as file:
                file.write(config + '\n')


def create_sub_section():
    readme_path = "README.md"
    sub_folder = "sub"
    found_sub_section = False

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as readme_file:
            content = readme_file.read()

            if '## Sub' in content:
                found_sub_section = True

    new_content = ""
    new_content += "## Sub\n"
    new_content += "| Sub |\n"
    new_content += "|-----|\n"

    for root, dirs, files in os.walk(sub_folder):
        for directory in dirs:
            config_path = os.path.join(root, directory, 'config.txt')
            if os.path.exists(config_path):
                url = f"https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/main/sub/{urllib.parse.quote(directory)}/config.txt"
                new_content += f"| [{directory}]({url}) |\n"

    with open(readme_path, 'w', encoding='utf-8') as readme_file:
        if found_sub_section:
            readme_file.write(content.replace(content[content.find('## Sub'):content.find('\n\n', content.find('## Sub'))], new_content))
        else:
            readme_file.write(content + new_content)

if __name__ == "__main__":
    telegram_urls = [
        "https://t.me/s/v2line",
        "https://t.me/s/forwardv2ray",
        "https://t.me/s/inikotesla",
        "https://t.me/s/PrivateVPNs",
        "https://t.me/s/VlessConfig",
        "https://t.me/s/V2pedia",
        "https://t.me/s/v2rayNG_Matsuri",
        "https://t.me/s/PrivateVPNs",
        "https://t.me/s/proxystore11",
        "https://t.me/s/DirectVPN",
        "https://t.me/s/VmessProtocol",
        "https://t.me/s/OutlineVpnOfficial",
        "https://t.me/s/networknim",
        "https://t.me/s/beiten",
        "https://t.me/s/MsV2ray",
        "https://t.me/s/foxrayiran",
        "https://t.me/s/DailyV2RY",
        "https://t.me/s/yaney_01",
        "https://t.me/s/FreakConfig",
        "https://t.me/s/EliV2ray",
        "https://t.me/s/ServerNett",
        "https://t.me/s/proxystore11",
        "https://t.me/s/v2rayng_fa2",
        "https://t.me/s/v2rayng_org",
        "https://t.me/s/V2rayNGvpni",
        "https://t.me/s/custom_14",
        "https://t.me/s/v2rayNG_VPNN",
        "https://t.me/s/v2ray_outlineir",
        "https://t.me/s/v2_vmess",
        "https://t.me/s/FreeVlessVpn",
        "https://t.me/s/vmess_vless_v2rayng",
        "https://t.me/s/PrivateVPNs",
        "https://t.me/s/freeland8",
        "https://t.me/s/vmessiran",
        "https://t.me/s/Outline_Vpn",
        "https://t.me/s/vmessq",
        "https://t.me/s/WeePeeN",
        "https://t.me/s/V2rayNG3",
        "https://t.me/s/ShadowsocksM",
        "https://t.me/s/shadowsocksshop",
        "https://t.me/s/v2rayan",
        "https://t.me/s/ShadowSocks_s",
        "https://t.me/s/VmessProtocol",
        "https://t.me/s/napsternetv_config",
        "https://t.me/s/Easy_Free_VPN",
        "https://t.me/s/V2Ray_FreedomIran",
        "https://t.me/s/V2RAY_VMESS_free",
        "https://t.me/s/v2ray_for_free",
        "https://t.me/s/V2rayN_Free",
        "https://t.me/s/free4allVPN",
        "https://t.me/s/vpn_ocean",
        "https://t.me/s/configV2rayForFree",
        "https://t.me/s/FreeV2rays",
        "https://t.me/s/DigiV2ray",
        "https://t.me/s/v2rayNG_VPN",
        "https://t.me/s/freev2rayssr",
        "https://t.me/s/v2rayn_server",
        "https://t.me/s/Shadowlinkserverr",
        "https://t.me/s/iranvpnet",
        "https://t.me/s/vmess_iran",
        "https://t.me/s/mahsaamoon1",
        "https://t.me/s/V2RAY_NEW",
        "https://t.me/s/v2RayChannel",
        "https://t.me/s/configV2rayNG",
        "https://t.me/s/config_v2ray",
        "https://t.me/s/vpn_proxy_custom",
        "https://t.me/s/vpnmasi",
        "https://t.me/s/v2ray_custom",
        "https://t.me/s/VPNCUSTOMIZE",
        "https://t.me/s/HTTPCustomLand",
        "https://t.me/s/vpn_proxy_custom",
        "https://t.me/s/ViPVpn_v2ray",
        "https://t.me/s/FreeNet1500",
        "https://t.me/s/v2ray_ar",
        "https://t.me/s/beta_v2ray",
        "https://t.me/s/vip_vpn_2022",
        "https://t.me/s/FOX_VPN66",
        "https://t.me/s/VorTexIRN",
        "https://t.me/s/YtTe3la",
        "https://t.me/s/V2RayOxygen",
        "https://t.me/s/Network_442",
        "https://t.me/s/VPN_443",
        "https://t.me/s/v2rayng_v",
        "https://t.me/s/ultrasurf_12",
        "https://t.me/s/iSeqaro",
        "https://t.me/s/frev2rayng",
        "https://t.me/s/frev2ray",
        "https://t.me/s/FreakConfig",
        "https://t.me/s/Awlix_ir",
        "https://t.me/s/v2rayngvpn",
        "https://t.me/s/God_CONFIG",
        "https://t.me/s/Configforvpn01",
    ]

    all_v2ray_configs = []
    for url in telegram_urls:
        v2ray_configs = get_v2ray_links(url)
        if v2ray_configs:
            all_v2ray_configs.extend(v2ray_configs)

    if all_v2ray_configs:
        save_configs_by_region(all_v2ray_configs)
        create_sub_section()
        print("Configs saved successfully.")
    else:
        print("No V2Ray configs found.")
