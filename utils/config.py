import os
import configparser
import shutil
import sys
import re


def resource_path(relative_path, persistent=False):
    """
    Get the resource path
    """
    base_path = os.path.abspath(".")
    total_path = os.path.join(base_path, relative_path)
    if persistent or os.path.exists(total_path):
        return total_path
    else:
        try:
            base_path = sys._MEIPASS
            return os.path.join(base_path, relative_path)
        except Exception:
            return total_path


def get_resolution_value(resolution_str):
    """
    Get resolution value from string
    """
    pattern = r"(\d+)[xX*](\d+)"
    match = re.search(pattern, resolution_str)
    if match:
        width, height = map(int, match.groups())
        return width * height
    else:
        return 0


class ConfigManager:

    def __init__(self):
        self.load()

    def __getattr__(self, name, *args, **kwargs):
        return getattr(self.config, name, *args, **kwargs)

    @property
    def open_service(self):
        return self.config.getboolean("Settings", "open_service", fallback=True)

    @property
    def open_update(self):
        return self.config.getboolean("Settings", "open_update", fallback=True)

    @property
    def open_filter_resolution(self):
        return self.config.getboolean(
            "Settings", "open_filter_resolution", fallback=True
        )

    @property
    def ipv_type(self):
        return self.config.get("Settings", "ipv_type", fallback="全部").lower()

    @property
    def ipv_type_prefer(self):
        return [
            type.strip().lower()
            for type in self.config.get(
                "Settings", "ipv_type_prefer", fallback="ipv4"
            ).split(",")
        ]

    @property
    def ipv4_num(self):
        return self.config.getint("Settings", "ipv4_num", fallback=15)

    @property
    def ipv6_num(self):
        return self.config.getint("Settings", "ipv6_num", fallback=15)

    @property
    def ipv_limit(self):
        return {
            "ipv4": self.ipv4_num,
            "ipv6": self.ipv6_num,
        }

    @property
    def origin_type_prefer(self):
        return [
            origin.strip().lower()
            for origin in self.config.get(
                "Settings",
                "origin_type_prefer",
                fallback="subscribe,hotel,multicast,online_search",
            ).split(",")
            if origin.strip().lower()
        ]

    @property
    def hotel_num(self):
        return self.config.getint("Settings", "hotel_num", fallback=10)

    @property
    def multicast_num(self):
        return self.config.getint("Settings", "multicast_num", fallback=10)

    @property
    def subscribe_num(self):
        return self.config.getint("Settings", "subscribe_num", fallback=10)

    @property
    def online_search_num(self):
        return self.config.getint("Settings", "online_search_num", fallback=10)

    @property
    def source_limits(self):
        return {
            "hotel": self.hotel_num,
            "multicast": self.multicast_num,
            "subscribe": self.subscribe_num,
            "online_search": self.online_search_num,
        }

    @property
    def min_resolution(self):
        return self.config.get("Settings", "min_resolution", fallback="1920x1080")

    @property
    def min_resolution_value(self):
        return get_resolution_value(self.min_resolution)

    @property
    def urls_limit(self):
        return self.config.getint("Settings", "urls_limit", fallback=30)

    @property
    def open_url_info(self):
        return self.config.getboolean("Settings", "open_url_info", fallback=True)

    @property
    def recent_days(self):
        return self.config.getint("Settings", "recent_days", fallback=30)

    @property
    def domain_blacklist(self):
        return [
            domain.strip()
            for domain in self.config.get(
                "Settings", "domain_blacklist", fallback=""
            ).split(",")
            if domain.strip()
        ]

    @property
    def url_keywords_blacklist(self):
        return [
            keyword.strip()
            for keyword in self.config.get(
                "Settings", "url_keywords_blacklist", fallback=""
            ).split(",")
            if keyword.strip()
        ]

    @property
    def source_file(self):
        return self.config.get("Settings", "source_file", fallback="config/demo.txt")

    @property
    def final_file(self):
        return self.config.get("Settings", "final_file", fallback="output/result.txt")

    @property
    def open_m3u_result(self):
        return self.config.getboolean("Settings", "open_m3u_result", fallback=True)

    @property
    def open_keep_all(self):
        return self.config.getboolean("Settings", "open_keep_all", fallback=False)

    @property
    def open_subscribe(self):
        return self.config.getboolean("Settings", f"open_subscribe", fallback=True)

    @property
    def open_hotel(self):
        return self.config.getboolean("Settings", f"open_hotel", fallback=True)

    @property
    def open_hotel_fofa(self):
        return self.config.getboolean("Settings", f"open_hotel_fofa", fallback=True)

    @property
    def open_hotel_tonkiang(self):
        return self.config.getboolean("Settings", f"open_hotel_tonkiang", fallback=True)

    @property
    def open_multicast(self):
        return self.config.getboolean("Settings", f"open_multicast", fallback=True)

    @property
    def open_multicast_fofa(self):
        return self.config.getboolean("Settings", f"open_multicast_fofa", fallback=True)

    @property
    def open_multicast_tonkiang(self):
        return self.config.getboolean(
            "Settings", f"open_multicast_tonkiang", fallback=True
        )

    @property
    def open_online_search(self):
        return self.config.getboolean("Settings", f"open_online_search", fallback=True)

    @property
    def open_method(self):
        return {
            "subscribe": self.open_subscribe,
            "hotel": self.open_hotel,
            "multicast": self.open_multicast,
            "online_search": self.open_online_search,
            "hotel_fofa": self.open_hotel_fofa,
            "hotel_tonkiang": self.open_hotel_tonkiang,
            "multicast_fofa": self.open_multicast_fofa,
            "multicast_tonkiang": self.open_multicast_tonkiang,
        }

    @property
    def open_use_old_result(self):
        return self.config.getboolean("Settings", "open_use_old_result", fallback=True)

    @property
    def open_sort(self):
        return self.config.getboolean("Settings", "open_sort", fallback=True)

    @property
    def open_ffmpeg(self):
        return self.config.getboolean("Settings", "open_ffmpeg", fallback=True)

    @property
    def open_update_time(self):
        return self.config.getboolean("Settings", "open_update_time", fallback=True)

    @property
    def multicast_region_list(self):
        return [
            region.strip()
            for region in self.config.get(
                "Settings", "multicast_region_list", fallback="全部"
            ).split(",")
            if region.strip()
        ]

    @property
    def hotel_region_list(self):
        return [
            region.strip()
            for region in self.config.get(
                "Settings", "hotel_region_list", fallback="全部"
            ).split(",")
            if region.strip()
        ]

    @property
    def request_timeout(self):
        return self.config.getint("Settings", "request_timeout", fallback=10)

    @property
    def sort_timeout(self):
        return self.config.getint("Settings", "sort_timeout", fallback=10)

    @property
    def open_proxy(self):
        return self.config.getboolean("Settings", "open_proxy", fallback=False)

    @property
    def open_driver(self):
        return self.config.getboolean("Settings", "open_driver", fallback=True)

    @property
    def hotel_page_num(self):
        return self.config.getint("Settings", "hotel_page_num", fallback=1)

    @property
    def multicast_page_num(self):
        return self.config.getint("Settings", "multicast_page_num", fallback=1)

    @property
    def online_search_page_num(self):
        return config.getint("Settings", "online_search_page_num", fallback=1)

    @property
    def subscribe_urls(self):
        return [
            url.strip()
            for url in self.config.get("Settings", "subscribe_urls", fallback="").split(
                ","
            )
            if url.strip()
        ]

    @property
    def response_time_weight(self):
        return self.config.getfloat("Settings", "response_time_weight", fallback=0.5)

    @property
    def resolution_weight(self):
        return self.config.getfloat("Settings", "resolution_weight", fallback=0.5)

    def load(self):
        """
        Load the config
        """
        self.config = configparser.ConfigParser()
        user_config_path = resource_path("config/user_config.ini")
        default_config_path = resource_path("config/config.ini")

        config_files = [user_config_path, default_config_path]
        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, "r", encoding="utf-8") as f:
                    self.config.read_file(f)
                break

    def set(self, section, key, value):
        """
        Set the config
        """
        self.config.set(section, key, value)

    def save(self):
        """
        Save config with write
        """
        user_config_file = "config/" + (
            "user_config.ini"
            if os.path.exists(resource_path("user_config.ini"))
            else "config.ini"
        )
        user_config_path = resource_path(user_config_file, persistent=True)
        if not os.path.exists(user_config_path):
            os.makedirs(os.path.dirname(user_config_path), exist_ok=True)
        with open(user_config_path, "w", encoding="utf-8") as configfile:
            self.config.write(configfile)

    def copy(self):
        """
        Copy config files to current directory
        """
        user_source_file = resource_path(
            self.config.get("Settings", "source_file", fallback="config/demo.txt")
        )
        user_config_path = resource_path("config/user_config.ini")
        default_config_path = resource_path("config/config.ini")
        user_config_file = (
            user_config_path
            if os.path.exists(user_config_path)
            else default_config_path
        )
        dest_folder = os.path.join(os.getcwd(), "config")
        files_to_copy = [user_source_file, user_config_file]
        try:
            if os.path.exists(dest_folder):
                if not os.path.isdir(dest_folder):
                    os.remove(dest_folder)
                    os.makedirs(dest_folder, exist_ok=True)
            else:
                os.makedirs(dest_folder, exist_ok=True)
            for src_file in files_to_copy:
                dest_path = os.path.join(dest_folder, os.path.basename(src_file))
                if os.path.abspath(src_file) == os.path.abspath(
                    dest_path
                ) or os.path.exists(dest_path):
                    continue
                shutil.copy(src_file, dest_folder)
            src_rtp_dir = resource_path("config/rtp")
            dest_rtp_dir = os.path.join(dest_folder, "rtp")
            if os.path.exists(src_rtp_dir):
                if not os.path.exists(dest_rtp_dir):
                    os.makedirs(dest_rtp_dir, exist_ok=True)

                for root, _, files in os.walk(src_rtp_dir):
                    for file in files:
                        src_file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(src_file_path, src_rtp_dir)
                        dest_file_path = os.path.join(dest_rtp_dir, relative_path)

                        dest_file_dir = os.path.dirname(dest_file_path)
                        if not os.path.exists(dest_file_dir):
                            os.makedirs(dest_file_dir, exist_ok=True)

                        if not os.path.exists(dest_file_path):
                            shutil.copy(src_file_path, dest_file_path)
        except Exception as e:
            print(f"Failed to copy files: {str(e)}")


config = ConfigManager()