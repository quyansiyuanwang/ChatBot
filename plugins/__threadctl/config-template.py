# 线程池相关配置, 该参数决定机器人可以同时处理几个人的消息, 超出线程池数量的请求会被阻塞, 不会被丢弃, 如果你不清楚该参数的意义, 请不要更改
# 线程池不完全支持热重载, 其中系统线程不支持重载, 管理员线程和用户线程可能需要在第二次热重载时才会更新配置, 但由于线程池本体足够使用, 暂不考虑完善此处
sys_pool_num = 8
# 执行管理员请求和指令的线程池并行线程数量, 一般和管理员数量相等
admin_pool_num = 2
# 执行用户请求和指令的线程池并行线程数量, 如需要更高的并发, 可以增大该值
user_pool_num = 6
