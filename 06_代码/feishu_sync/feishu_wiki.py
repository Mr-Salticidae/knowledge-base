# -*- coding: utf-8 -*-
"""
飞书 Wiki / 导入 / docx 操作层(Pass 1/2 用),基于 FeishuClient。

⚠️ 凡标注「# 待真机验证」的端点/字段,需在 POC 首跑时按真机返回校准。
   未拿到知识库成员权限前无法联调,这里按飞书开放平台文档实现。

文档内容上墙的链路(每篇):
  md 文本 → 上传素材(ccm_import_open) → 创建导入任务 → 轮询拿 docx token
         → move_docs_to_wiki 挂到 wiki 父节点 → 得 wiki node_token
目录节点:create wiki node(obj_type=docx 空占位)作为分组父节点。
双链回填:get blocks → 找 link.url 前缀=TEMP_PREFIX 的文本元素 → PATCH 改 url。
"""
import time
from feishu_client import FeishuClient, BASE


class FeishuWiki:
    def __init__(self, client=None, space_id=None):
        self.c = client or FeishuClient()
        self.space_id = space_id or self.c.cfg.get("target_space_id")
        self.domain = self.c.cfg.get("tenant_domain")  # 如 ncnnb044q88x.feishu.cn

    # ---------- 导入:md → docx ----------
    def upload_media_for_import(self, file_name, data_bytes,
                                file_extension="md", obj_type="docx"):
        """上传素材供导入用,返回 file_token。
        关键:parent_type=ccm_import_open 且必须带 extra(否则 1061004 forbidden)。"""
        import requests, json as _json
        files = {
            "file_name": (None, file_name),
            "parent_type": (None, "ccm_import_open"),
            "size": (None, str(len(data_bytes))),
            "extra": (None, _json.dumps({"obj_type": obj_type,
                                         "file_extension": file_extension})),
            "file": (file_name, data_bytes),
        }
        r = requests.post(f"{BASE}/drive/v1/medias/upload_all",
                          headers={"Authorization": f"Bearer {self.c.token()}"},
                          files=files, timeout=120)
        d = r.json()
        if d.get("code") != 0:
            raise RuntimeError(f"上传素材失败: {d}")
        return d["data"]["file_token"]

    def create_import_task(self, file_token, file_name, mount_folder_token,
                           file_extension="md", doc_type="docx"):
        """创建导入任务,返回 ticket。# 待真机验证(point.mount_type/mount_key)"""
        body = {
            "file_extension": file_extension,
            "file_token": file_token,
            "type": doc_type,
            "file_name": file_name,
            "point": {"mount_type": 1, "mount_key": mount_folder_token},
        }
        code, d = self.c.post("/drive/v1/import_tasks", json=body)
        if d.get("code") != 0:
            raise RuntimeError(f"创建导入任务失败: {d}")
        return d["data"]["ticket"]

    def poll_import(self, ticket, timeout=120, interval=2):
        """轮询导入任务,成功返回 (docx_token, url)。job_status==0 视为成功。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            code, d = self.c.get(f"/drive/v1/import_tasks/{ticket}")
            res = d.get("data", {}).get("result", {})
            st = res.get("job_status")
            if st == 0:  # 成功
                return res.get("token"), res.get("url")
            if st not in (None, 1, 2):  # 1=处理中 2=排队;其余视为失败
                raise RuntimeError(f"导入失败 status={st} msg={res.get('job_error_msg')}")
            time.sleep(interval)
        raise TimeoutError(f"导入任务超时 ticket={ticket}")

    # ---------- Wiki 节点 ----------
    def create_node(self, parent_node_token=None, title="", obj_type="docx",
                    node_type="origin"):
        """在知识空间建节点(用于目录分组占位)。返回 data(含 node_token/obj_token)。"""
        body = {"obj_type": obj_type, "node_type": node_type, "title": title}
        if parent_node_token:
            body["parent_node_token"] = parent_node_token
        code, d = self.c.post(f"/wiki/v2/spaces/{self.space_id}/nodes", json=body)
        if d.get("code") != 0:
            raise RuntimeError(f"建节点失败: {d}")
        return d["data"]["node"]

    def move_doc_to_wiki(self, obj_token, parent_wiki_token=None, obj_type="docx",
                         retries=4):
        """把已导入的 docx 挂进 wiki,返回 wiki_token。
        实测:首次可能异步返回空 wiki_token,重试即拿到(幂等)。"""
        body = {"obj_type": obj_type, "obj_token": obj_token}
        if parent_wiki_token:
            body["parent_wiki_token"] = parent_wiki_token
        last = None
        for _ in range(retries):
            code, d = self.c.post(
                f"/wiki/v2/spaces/{self.space_id}/nodes/move_docs_to_wiki", json=body)
            if d.get("code") != 0:
                raise RuntimeError(f"挂入wiki失败: {d}")
            wt = d["data"].get("wiki_token")
            if wt:
                return wt
            last = d
            time.sleep(1.5)
        raise RuntimeError(f"挂入wiki未返回wiki_token: {last}")

    # ---------- docx 块(双链回填) ----------
    def list_blocks(self, doc_id, page_size=500):
        blocks, token = [], None
        while True:
            params = {"page_size": page_size, "document_revision_id": -1}
            if token:
                params["page_token"] = token
            code, d = self.c.get(f"/docx/v1/documents/{doc_id}/blocks", params=params)
            if d.get("code") != 0:
                raise RuntimeError(f"取块失败: {d}")
            dd = d.get("data", {})
            blocks.extend(dd.get("items", []))
            token = dd.get("page_token")
            if not dd.get("has_more"):
                break
        return blocks

    def patch_block_elements(self, doc_id, block_id, elements):
        """整体替换某文本块的 elements(回填链接时用)。# 待真机验证(block 类型字段)"""
        body = {"update_text_elements": {"elements": elements}}
        code, d = self.c.req("PATCH",
                             f"/docx/v1/documents/{doc_id}/blocks/{block_id}", json=body)
        if d.get("code") != 0:
            raise RuntimeError(f"改块失败: {d}")
        return d["data"]

    # ---------- 图片嵌入 ----------
    def upload_docx_image(self, block_id, file_name, data_bytes):
        """上传图片到某图片块,返回 file_token。parent_type=docx_image。"""
        import requests
        files = {
            "file_name": (None, file_name),
            "parent_type": (None, "docx_image"),
            "parent_node": (None, block_id),
            "size": (None, str(len(data_bytes))),
            "file": (file_name, data_bytes, "image/png"),
        }
        r = requests.post(f"{BASE}/drive/v1/medias/upload_all",
                          headers={"Authorization": f"Bearer {self.c.token()}"},
                          files=files, timeout=180)
        d = r.json()
        if d.get("code") != 0:
            raise RuntimeError(f"上传图片失败: {d}")
        return d["data"]["file_token"]

    def set_image(self, doc_id, block_id, file_token):
        code, d = self.c.req(
            "PATCH", f"/docx/v1/documents/{doc_id}/blocks/{block_id}",
            json={"replace_image": {"token": file_token}})
        if d.get("code") != 0:
            raise RuntimeError(f"填图失败: {d}")

    def embed_images(self, doc_id, image_paths):
        """把本地图片按顺序嵌入文档里的图片占位块。
        策略:导入后每张图留一个空图块(type=27,尺寸是坏的默认值);
        删掉占位块→同位置新建空图块→上传图片(新块按图自然尺寸自适应)。
        倒序处理避免删块导致的 index 偏移。返回成功嵌入张数。"""
        import os
        blocks = self.list_blocks(doc_id)
        root = blocks[0]
        children = root.get("children", [])
        placeholders = [b for b in blocks if b.get("block_type") == 27]
        n = min(len(placeholders), len(image_paths))
        # 配对(按文档顺序),再按 index 倒序处理
        pairs = []
        for i in range(n):
            bid = placeholders[i]["block_id"]
            idx = children.index(bid) if bid in children else None
            pairs.append((idx, bid, image_paths[i]))
        done = 0
        for idx, bid, imgpath in sorted(pairs, key=lambda x: -(x[0] or 0)):
            if idx is None or not os.path.exists(imgpath):
                continue
            # 删占位
            self.c.req("DELETE",
                       f"/docx/v1/documents/{doc_id}/blocks/{root['block_id']}"
                       f"/children/batch_delete",
                       json={"start_index": idx, "end_index": idx + 1})
            # 新建空图块
            code, d = self.c.post(
                f"/docx/v1/documents/{doc_id}/blocks/{root['block_id']}/children",
                json={"index": idx, "children": [{"block_type": 27,
                                                  "image": {"token": ""}}]})
            newid = d.get("data", {}).get("children", [{}])[0].get("block_id")
            if not newid:
                continue
            with open(imgpath, "rb") as f:
                data = f.read()
            ftok = self.upload_docx_image(newid, os.path.basename(imgpath), data)
            self.set_image(doc_id, newid, ftok)
            done += 1
        return done

    # ---------- 四层标注上色 ----------
    LAYER_COLOR = {"🟦": 5, "🟩": 4, "🟨": 3, "🟥": 1}

    def colorize_layer_blocks(self, doc_id):
        """把以 🟦🟩🟨🟥 开头的文本块整段上色,并去掉前导 emoji。返回上色条数。"""
        blocks = self.list_blocks(doc_id)
        done = 0
        for b in blocks:
            container = None
            for k, v in b.items():
                if isinstance(v, dict) and isinstance(v.get("elements"), list):
                    container = v
                    break
            if not container:
                continue
            elements = container["elements"]
            if not elements:
                continue
            first = elements[0].get("text_run")
            if not first:
                continue
            content = first.get("content", "")
            sq = content.lstrip()[:1]
            if sq not in self.LAYER_COLOR:
                continue
            color = self.LAYER_COLOR[sq]
            # 去掉前导 "🟦 "(含其后空格)
            first["content"] = content.replace(sq, "", 1).lstrip()
            # 给整块每个 text_run 上色
            for el in elements:
                tr = el.get("text_run")
                if not tr:
                    continue
                style = tr.setdefault("text_element_style", {})
                style["text_color"] = color
            self.patch_block_elements(doc_id, b["block_id"], elements)
            done += 1
        return done

    def delete_doc(self, doc_token):
        """删除 docx(连带其 wiki 节点),进回收站。"""
        code, d = self.c.req("DELETE", f"/drive/v1/files/{doc_token}",
                             params={"type": "docx"})
        return d.get("code") == 0

    def wiki_url(self, node_token):
        dom = self.domain or "feishu.cn"
        return f"https://{dom}/wiki/{node_token}"

    def app_root_folder(self):
        """取应用云空间根目录 token(导入挂载点)。"""
        code, d = self.c.get("/drive/explorer/v2/root_folder/meta")
        if d.get("code") != 0:
            raise RuntimeError(f"取根目录失败: {d}")
        return d["data"]["token"]
