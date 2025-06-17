# Базовый образ nginx на Alpine
FROM nginx:alpine

# Удаляем дефолтный конфигурационный файл
RUN rm /etc/nginx/conf.d/default.conf


# Открываем порт 80 для входящих соединений
EXPOSE 80

# Запуск nginx в foreground режиме
CMD ["nginx", "-g", "daemon off;"]