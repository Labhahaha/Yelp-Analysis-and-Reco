# Yelp-Analysis-and-Reco
A project to analysis the data of yelp dataset and recomdation for consumers

项目框架的说明：
project/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── utils.py
│   │
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
│
└── README.md

backend/: Flask后端项目的目录。
    app/: Flask应用程序的主目录。
        __init__.py: 初始化Flask应用程序并配置相关设置，包括CORS配置。
        models.py: 定义数据库模型和相关操作。
        routes.py: 定义API路由和视图函数，处理来自前端的请求。
        utils.py: 存放辅助函数和工具类。
    config.py: Flask应用程序的配置文件。
    requirements.txt: Flask项目的依赖包列表。
    run.py: Flask应用程序的入口文件，用于启动后端服务器。
