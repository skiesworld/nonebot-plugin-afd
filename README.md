# nonebot-plugin-afd

基于NoneBot的自动审核爱发电订单号进群的插件

## 安装

- NoneBot2 插件商店安装
  ```shell
  nb plugin install nonebot-plugin-afd
  ```
  启动 `NoneBot2` 项目：`nb run`

## 配置

```json
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
