<div align="center">

# astrbot_plugin_autobangumi_command

**AutoBangumi 遥控器 — 聊天就能追番**

在 QQ/Telegram/微信 里发命令，直接操控 AutoBangumi 搜索、订阅、管理番剧

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D4.27.2-orange.svg)](https://github.com/AstrBotDevs/AstrBot)
[![AutoBangumi](https://img.shields.io/badge/AutoBangumi-required-red.svg)](https://github.com/EstrellaXD/Auto_Bangumi)

</div>

---

> **前置依赖**：本插件是 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 的插件，需要配合 [AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) 使用。

## 命令

| 命令 | 用法 | 说明 |
|------|------|------|
| `/search` | `/search 鬼灭之刃` | 在 Mikan 搜索番剧 |
| `/sub` | `/sub <Mikan RSS URL>` | 添加 RSS 订阅 |
| `/list` | `/list` | 查看所有订阅 |
| `/delete` | `/delete <ID>` | 删除指定订阅 |

## 快速开始

### 1. 安装

将插件文件夹放入 AstrBot 插件目录：

```
<AstrBot 数据目录>/data/plugins/astrbot_plugin_autobangumi_command/
```

### 2. 配置

打开 AstrBot WebUI → 插件设置 → `astrbot_plugin_autobangumi_command`：

| 配置项 | 说明 |
|--------|------|
| `ab_url` | AutoBangumi 访问地址，如 `http://192.168.1.20:7892` |
| `ab_username` | AutoBangumi 用户名 |
| `ab_password` | AutoBangumi 密码 |

### 3. 使用

在聊天中发送命令即可：

```
/search 鬼灭之刃
/sub https://mikanani.me/RSS/MyBangumi/xxx
/list
/delete 3
```

## 推荐搭配

| 插件 | 说明 |
|------|------|
| [astrbot_plugin_autobangumi_notify](https://github.com/Yometenma/astrbot_plugin_autobangumi_notify) | 通知转发——AutoBangumi 有新番时推送到聊天 |
| 本插件 | 遥控管理——在聊天中搜索、订阅、删除番剧 |

## 许可

MIT © yometenma
