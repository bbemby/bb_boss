# 🌸 bb_boss

> 本项目基于 [berry8838/Sakura_embyboss](https://github.com/berry8838/Sakura_embyboss) 修改，新增 `/user/whitelist` 接口供 [cfqm](https://github.com/bbemby/cfqm) 查询白名单用户。

<p align="center">
<img src="image/bot2.png" alt="bot"><br>
<a href="https://github.com/berry8838/Sakura_embyboss/stargazers"><img src="https://img.shields.io/github/stars/berry8838/Sakura_embyboss" alt="stars"></a> 
<a href="https://github.com/berry8838/Sakura_embyboss/forks"><img src="https://img.shields.io/github/forks/berry8838/Sakura_embyboss" alt="forks"></a> 
<a href="https://github.com/berry8838/Sakura_embyboss/issues"><img src="https://img.shields.io/github/issues/berry8838/Sakura_embyboss" alt="issue"></a>  
<a href="https://github.com/berry8838/Sakura_embyboss/blob/master/LICENSE"><img src="https://img.shields.io/github/license/berry8838/Sakura_embyboss" alt="license"></a> 
<a href="https://hub.docker.com/r/jingwei520/sakura_embyboss" ><img src="https://img.shields.io/docker/v/jingwei520/sakura_embyboss/latest?logo=docker" alt="docker"></a>
<a href="https://hub.docker.com/r/jingwei520/sakura_embyboss/tags" ><img src="https://img.shields.io/badge/platform-amd64%20arm64-pink" alt="plat"></a>
<a href="https://github.com/berry8838/Sakura_embyboss/actions/workflows/publish-docker_on_master.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/berry8838/Sakura_embyboss/publish-docker_on_master.yml?branch=master" alt="Build status" />
</a>
</p>
<br>

## 📜 项目说明

- **用 Telegram 管理 Emby 用户**（开服）
- **推荐使用 Debian 11 操作系统，AMD 处理器架构。目前 ARM 也支持（如有问题请反馈 issue）**
- 本项目基于 [berry8838/Sakura_embyboss](https://github.com/berry8838/Sakura_embyboss) 修改，新增 `/user/whitelist` 接口供 [cfqm](https://github.com/bbemby/cfqm) 查询白名单用户
- 反馈请尽量 issue，看到会处理

> **声明：本项目仅供学习交流使用，仅作为辅助工具借助 tg 平台方便用户管理自己的媒体库成员，对用户的其他行为及内容毫不知情**

---

## 🚀 部署教程

> 以下内容根据 [Sakura_embyboss Wiki](https://berry8838.github.io/Sakura_embyboss/deploy/introduce/) 整理并适配到本仓库。

### 一、部署方式选择

推荐 **Docker Compose** 部署，维护简单。如需魔改或二次开发，可选择 **源码部署**。

---

### 二、Docker Compose 部署

#### 1. 安装 Docker

```bash
curl -fsSL https://get.docker.com | bash -s docker
curl -L "https://github.com/docker/compose/releases/download/v2.10.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
systemctl start docker
systemctl enable docker
```

#### 2. 拉取代码

```bash
git clone https://github.com/bbemby/bb_boss.git /root/bb_boss
cd /root/bb_boss
chmod +x main.py
```

#### 3. 复制配置模板

```bash
cp config_example.json config.json
```

#### 4. 填写 config.json

**必填项：**

| 类型 | 字段 | 说明 |
|---|---|---|
| Telegram Bot | `bot_name` | Bot 的 username |
| | `bot_token` | 从 [@BotFather](https://t.me/BotFather) 获取 |
| | `owner_api` / `owner_hash` | 从 [my.telegram.org](https://my.telegram.org/auth) 获取 |
| | `owner` | 拥有者的 Telegram 用户 ID |
| | `group` | 授权管理群组 ID，如 `[-1001869392674]` |
| | `main_group` / `chanel` | 群组/频道 username 或邀请链接后缀 |
| Emby | `emby_api` | Emby API Key |
| | `emby_url` | Emby 访问地址，末尾不带 `/` |
| | `emby_line` | 展示给普通用户的 Emby 地址（MarkdownV2） |
| MySQL | `db_host` / `db_user` / `db_pwd` / `db_name` / `db_port` | 数据库连接信息 |

**自动更新：** 本仓库 `auto_update.git_repo` 已改为 `bbemby/bb_boss`，魔改用户请保持此值，以免被原仓库覆盖。

#### 5. 启动

```bash
docker-compose up -d
```

查看日志：

```bash
docker logs -f embyboss
```

#### 6. 更新

```bash
cd /root/bb_boss
docker-compose down
docker-compose pull
docker-compose up -d
```

---

### 三、源码部署

```bash
sudo apt install python3-pip
git clone https://github.com/bbemby/bb_boss.git /root/bb_boss
cd /root/bb_boss
chmod +x main.py
pip3 install -r requirements.txt
```

准备 MySQL 后，复制并填写 `config.json`，然后试运行：

```bash
python3 main.py
```

无报错后配置 systemd：

```bash
mv embyboss.service /etc/systemd/system/embyboss.service
systemctl daemon-reload
systemctl start embyboss
systemctl enable embyboss
```

常用命令：

```bash
systemctl status embyboss
systemctl restart embyboss
journalctl -u embyboss -f
```

---

### 四、更新与维护

#### 源码更新

```bash
cd /root/bb_boss
git fetch --all
git reset --hard origin/master
git pull origin master
pip3 install -r requirements.txt
systemctl restart embyboss
```

> 警告：源码更新会覆盖本地代码修改，魔改用户请先备份。

#### 数据库备份

在 `config.json` 中开启：

```json
{
  "db_is_docker": true,
  "db_docker_name": "mysql",
  "db_backup_dir": "./db_backup",
  "db_backup_maxcount": 7,
  "schedall": { "backup_db": true }
}
```

#### 高风险操作前建议先备份

执行 `/paolu`、`/banall`、`/unbanall`、`/only_rm_emby`、`/only_rm_record`、`/coinsclear`、`/restore_from_db` 前建议先备份数据库。

---

### 五、常见问题

#### 1. 自动更新覆盖了本地修改

检查 `config.json` 中 `auto_update.git_repo` 是否为 `bbemby/bb_boss`。

#### 2. `/user/whitelist` 接口

用于 cfqm 查询白名单用户：

```
GET http://<服务器>:8838/user/whitelist?emby_id=<Emby用户名>&token=<bot_token>
```

返回：

```json
{"whitelist": true}   // 白名单用户（lv='a'）
{"whitelist": false}  // 非白名单用户
```

#### 3. cfqm 连接返回 403

`/user/*` 接口需要 `?token=<bot_token>` 鉴权，请在 cfqm 中配置 `EMBYBOSS_BOT_TOKEN`。

---

### 六、相关项目

- [cfqm](https://github.com/bbemby/cfqm) — Cloudflare Workers 版 Emby 事件通知中间层
- [berry8838/Sakura_embyboss](https://github.com/berry8838/Sakura_embyboss) — 原项目

<br>

## 💐 Our Contributors

<a href="https://github.com/berry8838/Sakura_embyboss/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=berry8838/Sakura_embyboss" />
</a>  

## 特别感谢（排序不分先后）<img src="image/bixin.jpg" alt="比心" height=30>

- [Pyrogram • 一个现代、优雅和异步的MTProto API框架](https://github.com/pyrogram/pyrogram)
- [Nezha探针 • 自托管、轻量级、服务器和网站监控运维工具](https://github.com/naiba/nezha)
- [小宝 • 按钮风格](https://t.me/EmbyClubBot)
- [MisakaF_Emby • 启发](https://github.com/MisakaFxxk/MisakaF_Emby)
  以及  [EMBY API官方文档](https://swagger.emby.media/?staticview=true#/UserService)
- [Nolovenodie • 播放榜单海报推送借鉴](https://github.com/Nolovenodie/EmbyTools)
- [罗宝 • 提供的代码援助](https://github.com/dddddluo)
- [折花 • 日榜周榜推送设计图](https://github.com/U41ovo)<br>


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=berry8838/Sakura_embyboss&type=Date)](https://star-history.com/#berry8838/Sakura_embyboss)