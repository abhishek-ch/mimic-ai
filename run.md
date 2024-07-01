
```shell
docker run -d -p 3100:8080 --add-host=host.docker.internal:host-gateway \
  -v /Users/gmcjy/Documents/sourcecode/MIMIC_DATA/landing/2.0:/app/local_data \
  -v mimicai:/app/backend/data \
  -v ./db:/app/db \
  --name mimicai --restart always buntha/mimicai:latest
```
