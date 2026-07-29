# bb_boss 部署教程

> 本项目基于 [berry8838/Sakura_embyboss](https://github.com/berry8838/Sakura_embyboss) 修改，新增 `/user/whitelist` 接口供 [cfqm](https://github.com/bbemby/cfqm) 查询白名单用户。  
> 以下内容根据 [Sakura_embyboss Wiki](https://berry8838.github.io/Sakura_embyboss/deploy/introduce/) 整理并适配到本仓库。

---

## 一、部署方式选择

推荐 **Docker Compose** 部署，维护简单。  
如需魔改或二次开发，可选择 **源码部署**。

---

## 二、Docker Compose 部署

### 1. 安装 Docker

```bash
curl -fsSL https://get.docker.com | bash -s docker
curl -L "https://github.com/docker/compose/releases/download/v2.10.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
systemctl start docker
systemctl enable docker
```

### 2. 拉取代码

```bash
git clone https://github.com/bbemby/bb_boss.git /root/bb_boss
cd /root/bb_boss
chmod +x main.py
```

### 3. 复制配置模板

```bash
cp config_example.json config.json
```

使用你熟悉的编辑器打开 `config.json`，按下面说明填写。

### 4. 填写 config.json

#### 必填项

| 类型 | 字段 | 说明 |
|---|---|---|
| Telegram Bot | `bot_name` | Bot 的 username，例如 `keaiji1_bot` |
| | `bot_token` | 从 [@BotFather](https://t.me/BotFather) 获取 |
| | `owner_api` | 从 [my.telegram.org](https://my.telegram.org/auth) 获取的 API ID |
| | `owner_hash` | 从 [my.telegram.org](https://my.telegram.org/auth) 获取的 API Hash |
| | `owner` | 拥有者的 Telegram 用户 ID（纯数字） |
| | `group` | 授权管理群组 ID，例如 `[-1001869392674]` |
| | `main_group` | 群组 username 或邀请链接后缀 |
| | `chanel` | 频道 username 或邀请链接后缀 |
| Emby | `emby_api` | Emby API Key |
| | `emby_url` | Emby 访问地址，例如 `http://127.0.0.1:8096` 或 `https://emby.xxx.com`，末尾不带 `/` |
| | `emby_line` | 展示给普通用户的 Emby 地址（Telegram MarkdownV2 写法） |
| MySQL | `db_host` / `db_user` / `db_pwd` / `db_name` / `db_port` | 数据库连接信息 |

#### 关于自动更新

本仓库是魔改版，`auto_update.git_repo` 已默认改为 `bbemby/bb_boss`：

```json
{
  "auto_update": {
    "status": true,
    "git_repo": "bbemby/bb_boss",
    "commit_sha": null,
    "up_description": null
  }
}
```

如果你继续用原仓库镜像，请改回 `berry8838/Sakura_embyboss`；如果希望自己 fork 维护，改成你自己的仓库名。

### 5. 启动 MySQL 与 Bot

```bash
docker-compose up -d
```

查看日志：

```bash
docker logs -f embyboss
```

### 6. Docker 更新

```bash
cd /root/bb_boss
docker-compose down
docker-compose pull
docker-compose up -d
```

---

## 三、源码部署

### 1. 拉取代码

```bash
sudo apt install python3-pip
git clone https://github.com/bbemby/bb_boss.git /root/bb_boss
cd /root/bb_boss
chmod +x main.py
```

### 2. 准备 MySQL

可自己选择安装方式（宝塔、Docker、apt 等）。Docker 方式示例：

```bash
cd /root/bb_boss
docker-compose up mysql -d
```

### 3. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 4. 填写 config.json

同 Docker 部署第 4 步。

### 5. 试运行

```bash
python3 main.py
```

确认无报错后，按 `Ctrl+C` 停止，继续配置 systemd。

### 6. 配置 systemd 守护程序

编辑 `embyboss.service`，按实际路径修改后：

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
systemctl stop embyboss
journalctl -u embyboss -f
```

---

## 四、更新与维护

### 源码更新

```bash
cd /root/bb_boss
git fetch --all
git reset --hard origin/master
git pull origin master
pip3 install -r requirements.txt
systemctl restart embyboss
```

> 警告：源码更新会覆盖本地代码修改，魔改用户请先备份或使用自己的分支。

### 数据库备份

在 `config.json` 中开启：

```json
{
  "db_is_docker": true,
  "db_docker_name": "mysql",
  "db_backup_dir": "./db_backup",
  "db_backup_maxcount": 7,
  "schedall": {
    "backup_db": true
  }
}
```

或在 Telegram 中由 owner 执行 `/backup_db`。

### 高风险操作前建议先备份

执行以下命令前建议先备份数据库：

- `/paolu`
- `/banall`
- `/unbanall`
- `/only_rm_emby`
- `/only_rm_record`
- `/coinsclear`
- `/restore_from_db`

---

## 五、常见问题

### 1. 自动更新拉取原仓库覆盖了我的修改

请检查 `config.json` 中 `auto_update.git_repo` 是否改成了你自己的仓库，例如 `bbemby/bb_boss`。

### 2. 找不到 `/user/whitelist` 接口

本仓库已内置该接口，用于 cfqm 查询白名单用户。接口地址：

```
GET http://<你的服务器>:8838/user/whitelist?emby_id=<Emby用户名>&token=<bot_token>
```

返回：

```json
{"whitelist": true}   // 白名单用户（lv='a'）
{"whitelist": false}  // 非白名单用户
```

如果接口不存在，请确认代码已更新到最新版本。

### 3. cfqm 连接本接口返回 403

因为 `/user/*` 接口默认需要 `?token=<bot_token>` 鉴权。请在 cfqm 中配置 `EMBYBOSS_BOT_TOKEN` 为你的 `bot_token`。

---

## 六、相关项目

- [cfqm](https://github.com/bbemby/cfqm) — Cloudflare Workers 版 Emby 事件通知中间层，可联动本仓库实现白名单用户特殊称呼。
- [berry8838/Sakura_embyboss](https://github.com/berry8838/Sakura_embyboss) — 原项目。
