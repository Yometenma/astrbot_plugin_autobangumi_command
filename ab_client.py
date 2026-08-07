"""AutoBangumi HTTP API 客户端。"""

import logging
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)


class ABCLient:
    """AutoBangumi REST API 客户端。"""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self._token: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _ensure_auth(self) -> None:
        if self._token:
            return
        session = await self._get_session()
        try:
            async with session.post(
                f"{self.base_url}/api/v1/auth/login",
                data={"username": self.username, "password": self.password},
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self._token = data.get("access_token")
                    logger.info("AutoBangumi 认证成功")
                else:
                    raise RuntimeError(f"认证失败: HTTP {resp.status}")
        except Exception as e:
            logger.error(f"AutoBangumi 认证失败: {e}")
            raise

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        await self._ensure_auth()
        session = await self._get_session()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._token}"
        url = f"{self.base_url}{path}"
        async with session.request(method, url, headers=headers, **kwargs) as resp:
            if resp.status == 401:
                self._token = None
                return await self._request(method, path, **kwargs)
            if resp.status >= 400:
                text = await resp.text()
                raise RuntimeError(f"API 错误 [{method} {path}]: {resp.status} {text[:200]}")
            return await resp.json()

    async def list_rss(self) -> list[dict]:
        """获取所有 RSS 订阅。"""
        return await self._request("GET", "/api/v1/rss")

    async def add_rss(self, url: str, name: str = "", parser: str = "mikan") -> dict:
        """添加 RSS 订阅。"""
        return await self._request("POST", "/api/v1/rss/add", json={
            "url": url,
            "name": name,
            "aggregate": True,
            "parser": parser,
        })

    async def delete_rss(self, rss_id: int) -> dict:
        """删除 RSS 订阅。"""
        return await self._request("DELETE", f"/api/v1/rss/delete/{rss_id}")

    async def search(self, keywords: str) -> list[dict]:
        """搜索番剧。"""
        result = await self._request("GET", "/api/v1/search/bangumi", params={
            "site": "mikan",
            "keywords": keywords,
        })
        return result if isinstance(result, list) else []

    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None
