# 智能家居
  
  exten 与项目无关文件
    nginx.conf nginx相关配置
    
  uwsgi.ini 服务器配置
  
  requirements.txt 项目相关依赖
  
  venv python虚拟环境
    . /venv/bin/active 进入
    deactived 退出虚拟环境
    
    
    
  manage.py 开发测试使用
    python manage.py runserver -h 192.168.0.147
    
  release.py 生产环境使用
    uwsgi uwsgi.ini 开启服务器
    
    
  