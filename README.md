# nonebot-plugin-afd

基于NoneBot的自动审核爱发电订单号进群的插件

## 安装

- 适配器
    - [`nonebot-adapter-onebot`](https://github.com/nonebot/adapter-onebot)
    - [`nonebot-adapter-afdian`](https://github.com/MineGraphCN/nonebot-adapter-afdian)

- NoneBot2 插件商店安装
  ```shell
  nb plugin install nonebot-plugin-afd
  ```
  启动 `NoneBot2` 项目：`nb run`

## 配置

```
# 插件配置
afd_token_list = '{
    "群号": ["作者1user_id", "作者2user_id"]
}'

# 适配器配置
afdian_bots='[
    {
        "user_id": "爱发电开发者页面user_id",
        "api_token": "爱发电开发者页面api_token"
    }
]'
```

## 使用

1. 给Bot管理员身份
2. 设置加群验证方式为：`需要回答问题并由管理员审核`
3. 用户加群，**仅需**填写 `订单号` 即可（**不要填入其他任何字符**）

# 特别感谢

- [NoneBot2](https://github.com/nonebot/nonebot2)：开发框架。

## 贡献与支持

觉得好用可以给这个项目点个 `Star` 或者去 [爱发电](https://afdian.net/a/17TheWord) 投喂我。

有意见或者建议也欢迎提交 [Issues](https://github.com/17TheWord/nonebot-plugin-afd/issues)
和 [Pull requests](https://github.com/17TheWord/nonebot-plugin-afd/pulls) 。

## 开源许可

本项目使用 [MIT](./LICENSE) 作为开源许可证。

