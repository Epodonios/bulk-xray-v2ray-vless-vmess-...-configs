import requests
from bs4 import BeautifulSoup
import os
import shutil
import re
import json
import urllib.parse
from functools import lru_cache
#Improved V2Ray Scraper with Region Categorization and README Automation

# Improvements Summary:
# Feature	        Old Version	        New Version
# IP Extraction	    Fragile	            Regex + URI parsing
# API Handling	    Naive	            Cached + fault-tolerant
# Markdown Update	Risky	            Safe append/replace
# Logging & Errors	Minimal	            Clear [INFO] / [ERROR] messages
# File Handling	    Manual	            Auto-create & clean folders


# --- Configuration ---
TELEGRAM_CHANNELS = [
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
CONFIG_DIR = "sub"
README_FILE = "README.md"
RAW_GITHUB_BASE = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/sub/"  # Change this

# --- Step 1: Extract Config Links ---
def get_v2ray_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        tags = soup.find_all(['div', 'span', 'code'])
        links = []

        for tag in tags:
            text = tag.get_text().strip()
            match = re.findall(r'(vless|vmess|ss|trojan|tuic)://[^\s<>\"]+', text)
            links.extend(match if isinstance(match, list) else [match])

        return list(set(links))  # Remove duplicates
    except Exception as e:
        print(f"[ERROR] Failed to process {url}: {e}")
        return []

# --- Step 2: Extract IP or Domain from Config ---
def extract_host(config_link):
    try:
        parsed = urllib.parse.urlparse(config_link)
        if parsed.netloc:
            return parsed.netloc.split('@')[-1].split(':')[0]
        elif parsed.path:
            return parsed.path.split('@')[-1].split(':')[0]
    except Exception:
        return None

# --- Step 3: Get Country from IP/Domain ---
@lru_cache(maxsize=512)
def get_region_from_ip(ip_or_domain):
    endpoints = [
        f'https://ipapi.co/{ip_or_domain}/json/',
        f'https://ipwho.is/{ip_or_domain}',
        f'http://ip-api.com/json/{ip_or_domain}',
    ]
    for endpoint in endpoints:
        try:
            res = requests.get(endpoint, timeout=8)
            if res.status_code == 200:
                data = res.json()
                country = data.get('country_name') or data.get('country')
                if country:
                    return country.replace(" ", "_")
        except Exception:
            continue
    return "Unknown"

# --- Step 4: Save Configs by Region ---
def save_configs_by_region(configs):
    if os.path.exists(CONFIG_DIR):
        shutil.rmtree(CONFIG_DIR)
    os.makedirs(CONFIG_DIR, exist_ok=True)

    for config in configs:
        host = extract_host(config)
        if not host:
            continue
        region = get_region_from_ip(host)
        region_folder = os.path.join(CONFIG_DIR, region)
        os.makedirs(region_folder, exist_ok=True)
        file_path = os.path.join(region_folder, "config.txt")
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(config + '\n')

# --- Step 5: Update README.md ---
def create_sub_section():
    table = "\n## Sub\n| Region | Link |\n|--------|------|\n"
    for region in sorted(os.listdir(CONFIG_DIR)):
        config_path = os.path.join(CONFIG_DIR, region, 'config.txt')
        if os.path.exists(config_path):
            link = f"{RAW_GITHUB_BASE}{urllib.parse.quote(region)}/config.txt"
            table += f"| {region} | [config.txt]({link}) |\n"

    if os.path.exists(README_FILE):
        with open(README_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        if '## Sub' in content:
            pre = content.split('## Sub')[0]
            content = pre + table
        else:
            content += "\n" + table
    else:
        content = "# VPN Configs\n" + table

    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

# --- Main Program ---
if __name__ == "__main__":
    all_configs = []
    for url in TELEGRAM_CHANNELS:
        configs = get_v2ray_links(url)
        all_configs.extend(configs)

    if all_configs:
        print(f"[INFO] Found {len(all_configs)} configs.")
        save_configs_by_region(all_configs)
        create_sub_section()
        print("[SUCCESS] Configs saved and README updated.")
    else:
        print("[INFO] No configs found.")
