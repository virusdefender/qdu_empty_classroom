#青岛大学空教室查询

*app*目录是客户端，使用 http://dcloud.io/ 打包生成。供参考。

*server*目录是服务器端，部署在新浪云上，依赖kvdb。实现的比较简单，供参考。

*spider*目录是爬虫，使用Python线程池实现。命名规则是 `校区id.教学楼id.教学周.星期.json`，里面的数据是每个教室的数据，0代表没课，1代表有课。

更多介绍见 https://virusdefender.net/index.php/archives/197/
