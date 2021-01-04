# coding=utf-8
"""
@auth: xiaobei
@date: 2021/1/1
@desc:
"""
# coding: utf-8
# @File     :   config
import os

try:
    import ConfigParser
except:
    import configparser as ConfigParser

config = ConfigParser.ConfigParser()


def load_service_config():
    config_filename = os.path.join(os.path.dirname(__file__), 'config.ini').replace(r'\\', '/')
    config.read(config_filename)
    return config


service_config = load_service_config()

# 如果配置文件中没有给出日志路径，那么默认存储项目根目录
if not service_config.has_option('spider_settings', 'log_path'):
    service_config.set('spider_settings', 'log_path', os.path.dirname(__file__))

# 日志文件路径
LOG_PATH = service_config.get('spider_settings', 'log_path')


if __name__ == '__main__':
    print(LOG_PATH)
