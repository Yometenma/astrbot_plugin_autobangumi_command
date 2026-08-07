"""
astrbot_plugin_autobangumi_command
AutoBangumi 遥控插件 — 通过聊天命令操控 AutoBangumi

命令：
    /search <关键词>    搜索番剧
    /sub <Mikan URL>   添加 RSS 订阅
    /list               查看订阅列表
    /delete <ID>        删除订阅

作者：yometenma
版本：1.0.1
"""

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

from .ab_client import ABClient

__version__ = "1.0.1"

# LLM 转述任务指令
REPLY_TASK = "请用你的口吻回复这条消息。保持信息准确，语气自然。"


@register(
    "astrbot_plugin_autobangumi_command",
    "yometenma",
    "AutoBangumi 遥控器",
    __version__,
)
class AutoBangumiCommandPlugin(Star):
    """AutoBangumi 遥控插件。"""

    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.ab_url = str(config.get("ab_url", "http://127.0.0.1:7892"))
        self.ab_username = str(config.get("ab_username", "admin"))
        self.ab_password = str(config.get("ab_password", ""))
        self.use_llm = bool(config.get("use_llm", True))
        self._client: ABClient | None = None

    async def initialize(self) -> None:
        self._client = ABClient(self.ab_url, self.ab_username, self.ab_password)
        try:
            await self._client._ensure_auth()
            self.logger.info(f"已连接 AutoBangumi: {self.ab_url}")
        except Exception as e:
            self.logger.error(f"连接 AutoBangumi 失败: {e}")

    async def terminate(self) -> None:
        if self._client:
            await self._client.close()

    async def _reply(self, text: str) -> str:
        """用 AstrBot 自身人格转述回复文本。"""
        if not self.use_llm:
            return text
        try:
            provider = self.context.get_using_provider()
            if provider is None:
                return text
            resp = await provider.text_chat(
                prompt=text, system_prompt=REPLY_TASK,
            )
            if resp and resp.result_chain:
                plain = resp.result_chain.get_plain_text()
                return plain or text
        except Exception:
            pass
        return text

    # ==================== /search — 搜索番剧 ====================

    @filter.command("search")
    async def cmd_search(self, event: AstrMessageEvent, keywords: str = ""):
        if not keywords:
            yield event.plain_result("用法: /search <关键词>")
            return
        try:
            results = await self._client.search(keywords)
            if not results:
                msg = f"搜索「{keywords}」没有找到相关番剧"
                yield event.plain_result(await self._reply(msg))
                return
            lines = [f"搜索「{keywords}」结果:"]
            for i, item in enumerate(results[:10], 1):
                title = item.get("title", "未知")
                lines.append(f"{i}. {title}")
            yield event.plain_result(await self._reply("\n".join(lines)))
        except Exception as e:
            yield event.plain_result(await self._reply(f"搜索失败: {e}"))

    # ==================== /sub — 添加订阅 ====================

    @filter.command("sub")
    async def cmd_subscribe(self, event: AstrMessageEvent, url: str = ""):
        if not url:
            yield event.plain_result("用法: /sub <Mikan RSS URL> [名称]")
            return
        # 解析 URL 和可选名称
        parts = url.split(None, 1)
        rss_url = parts[0]
        name = parts[1].strip() if len(parts) > 1 else ""
        try:
            result = await self._client.add_rss(rss_url, name=name)
            msg = result.get("msg_zh", result.get("msg_en", "已添加"))
            yield event.plain_result(await self._reply(f"RSS 订阅结果: {msg}"))
        except Exception as e:
            yield event.plain_result(await self._reply(f"添加订阅失败: {e}"))

    # ==================== /list — 查看订阅 ====================

    @filter.command("list")
    async def cmd_list(self, event: AstrMessageEvent):
        try:
            items = await self._client.list_rss()
            if not items:
                yield event.plain_result(await self._reply("当前没有任何 RSS 订阅"))
                return
            lines = ["当前 RSS 订阅:"]
            for item in items:
                rss_id = item.get("id", "?")
                name = item.get("name") or item.get("url", "?")
                enabled = "✅" if item.get("enable", True) else "⏸"
                lines.append(f"  [{rss_id}] {enabled} {name}")
            yield event.plain_result(await self._reply("\n".join(lines)))
        except Exception as e:
            yield event.plain_result(await self._reply(f"获取订阅失败: {e}"))

    # ==================== /delete — 删除订阅 ====================

    @filter.command("delete")
    async def cmd_delete(self, event: AstrMessageEvent, rss_id: str = ""):
        if not rss_id:
            yield event.plain_result("用法: /delete <订阅ID>（通过 /list 查看）")
            return
        try:
            rss_id_int = int(rss_id)
        except ValueError:
            yield event.plain_result(f"无效的 ID：「{rss_id}」，请输入数字")
            return
        try:
            result = await self._client.delete_rss(rss_id_int)
            msg = result.get("msg_zh", result.get("msg_en", "已删除"))
            yield event.plain_result(await self._reply(f"删除订阅结果: {msg}"))
        except Exception as e:
            yield event.plain_result(await self._reply(f"删除订阅失败: {e}"))
