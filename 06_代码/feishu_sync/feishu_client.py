# -*- coding: utf-8 -*-
"""
飞书 API 客户端(Pass 1/2/同步器共用)

凭证来源(优先级):
1. 环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET
2. 同目录 feishu_config.json(已 gitignore,密钥不入库)

config 示例见 feishu_config.example.json
"""
import os
import json
import time
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "feishu_config.json")
BASE = "https://open.feishu.cn/open-apis"


def load_config():
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    app_id = os.environ.get("FEISHU_APP_ID") or cfg.get("app_id")
    app_secret = os.environ.get("FEISHU_APP_SECRET") or cfg.get("app_secret")
    if not app_id or not app_secret:
        raise SystemExit(
            "缺少凭证:请在 06_代码/feishu_sync/feishu_config.json 填入 "
            "app_id/app_secret(参考 feishu_config.example.json),"
            "或设置环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET。")
    cfg["app_id"] = app_id
    cfg["app_secret"] = app_secret
    return cfg


class FeishuClient:
    def __init__(self, cfg=None):
        self.cfg = cfg or load_config()
        self._token = None
        self._token_exp = 0

    # ---- 鉴权 ----
    def token(self):
        if self._token and time.time() < self._token_exp - 60:
            return self._token
        r = requests.post(
            f"{BASE}/auth/v3/tenant_access_token/internal",
            json={"app_id": self.cfg["app_id"],
                  "app_secret": self.cfg["app_secret"]},
            timeout=15)
        data = r.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取 tenant_access_token 失败: {data}")
        self._token = data["tenant_access_token"]
        self._token_exp = time.time() + data.get("expire", 7200)
        return self._token

    # ---- 通用请求 ----
    def req(self, method, path, **kw):
        headers = kw.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.token()}"
        url = path if path.startswith("http") else f"{BASE}{path}"
        r = requests.request(method, url, headers=headers, timeout=30, **kw)
        try:
            return r.status_code, r.json()
        except ValueError:
            return r.status_code, {"_raw": r.text}

    def get(self, path, **kw):
        return self.req("GET", path, **kw)

    def post(self, path, **kw):
        return self.req("POST", path, **kw)

    # ---- 便捷封装 ----
    def list_wiki_spaces(self, page_size=50):
        spaces, token = [], None
        while True:
            params = {"page_size": page_size}
            if token:
                params["page_token"] = token
            code, data = self.get("/wiki/v2/spaces", params=params)
            if data.get("code") != 0:
                return code, data, spaces
            d = data.get("data", {})
            spaces.extend(d.get("items", []))
            token = d.get("page_token")
            if not d.get("has_more"):
                break
        return 200, {"code": 0}, spaces


if __name__ == "__main__":
    c = FeishuClient()
    print("token ok:", c.token()[:12], "...")
