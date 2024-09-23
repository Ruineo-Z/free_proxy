FROM nginx:latest

# 设置上海时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 删除默认的配置文件
RUN rm /etc/nginx/conf.d/default.conf

RUN chmod -R 775 /var/log/nginx

# 复制自定义的 nginx.conf 文件到 Nginx 的配置目录
COPY nginx.conf /etc/nginx/conf.d/default.conf
