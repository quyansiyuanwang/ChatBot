from Models.Plugins import *

# 注册插件


@register(
    description="定时提醒",
    version="0.1",
    author="For_Lin0601",
    priority=10,
)
class TimeReminderPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_list):
        print("插件 TimedReminder 已加载")

    @on("timed_reminder")
    @on("fuck")
    def _1(self, event):
        print("定时提醒")

    @on("PersonMessage")
    def _2(self, event):
        print("好友消息")

    # 插件卸载时触发
    def __del__(self):
        pass
