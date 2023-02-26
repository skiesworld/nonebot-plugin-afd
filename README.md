# nonebot-plugin-afd

基于NoneBot的自动审核爱发电订单号进群的插件

## 安装

- 脚手架安装
  ```shell
    pip install nonebot-plugin-afd
    ```
    1. 在 `pyproject.toml` 文件 `plugins` 内填入插件名：`plugins = ["nonebot_plugin_afd"]`
    2. 启动 `NoneBot2` 项目：`nb run`

- NoneBot2 插件商店安装
  ```shell
  nb plugin install nonebot-plugin-afd
  ```
  启动 `NoneBot2` 项目：`nb run`

## 配置

```json
# 因 NoneBot读取配置文件问题，请填写完毕之后缩减至一行
AFD_TOKEN_LIST={
    "作者1的群号": {
        "user_id": "作者1 爱发电的 user_id",
        "token": "作者1 爱发电的 token"
    },
    "作者2的群号": {
        "user_id": "作者2 爱发电的 user_id",
        "token": "作者2 爱发电的 token"
    },
}
```
