<div align="center">
    <p align="center">
        <img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/c430bbf2-fa74-4235-b078-0f4b7b571353" alt="logo" width="500" />
    </p>
    
![GitHub License](https://img.shields.io/github/license/Labhahaha/Yelp-Analysis-and-Reco)
![Static Badge](https://img.shields.io/badge/collaborator-4-lightblue)
![python version](https://img.shields.io/badge/python-3.7-orange.svg)
![GitHub Repo stars](https://img.shields.io/github/stars/Labhahaha/Yelp-Analysis-and-Reco)

<h2 align="center">Yelp-Analysis-and-Reco</h2>
</div>

# ✨ 简介

这是yelp点评数据分析与推荐项目的后端仓库，是集成了协同过滤推荐算法、搜索算法和NLP情感分析算法的flask后端应用.

前端仓库请移步[Yelp-Analysis-and-Reco_frontend](https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend)．

# 🎉 特性

## 数据可视化

- 商户分析
- 用户分析
- 评论分析
- 评分分析
- 打卡分析

## 应用功能

- 用户端点评推荐
- 用户端商户搜索
- 用户端好友推荐
- 商家端经营推荐
- 评论情感分析

> [!Warning]
> 本项目使用的图标及首页图片等均来自[yelp官方网站](https://www.yelp.com/)，开源项目仅作学习交流之用，请遵守相关版权规定

# 🛠 技术栈

| [Flask](https://flask.palletsprojects.com/) | [PyTorch](https://pytorch.org) | [Scikit-learn](https://scikit-learn.org/stable/index.html) | [Scikit-surprise](https://surpriselib.com/) |
|:---:|:---:|:---:|:---:|
| [<img src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/3cd27a4b-7268-401a-afc9-ea9a118caa31" alt="flask" height="100px"/>](https://flask.palletsprojects.com/) | [<img src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/56c66fc1-0491-4eae-bad5-4c08115c4776" alt="pytorch" height="100px"/>](https://pytorch.org) | [<img src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/18254205-d00a-4f99-aa85-5e3d1dfbf1ab" alt="scikit-learn" height="80px"/>](https://scikit-learn.org/stable/index.html) | [<img src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/f9fa440c-871b-4e58-b253-50239cb8cf03" alt="scikit-surprise" height="50px"/>](https://surpriselib.com/) |



# 🚀 项目运行说明

## 安装依赖
```sh
pip install -r requirements.txt
```
> [!NOTE]
> torch版本请确保与设备显卡的CUDA版本匹配

## 项目设置
- 在`config/config.py`中填写你的数据库服务器地址和端口号
- 在`app/Advice/Boards.py`中填写你的文心一言API_TOKEN
- 在`config/model`中放置你的模型权重文件
> [!NOTE]
> 本项目的数据库是在[yelp开源数据库](https://www.yelp.com/dataset)的基础上进行了一些数据处理和筛选，新增了许多新的数据表
> 
> 项目所使用的数据库和预训练模型权重可通过Issue从开发者处获取，当然您也可以根据项目自行处理和训练

## 项目运行
```sh
python run.py
```
> [!Warning]
> 如遇项目报错`Resource averaged_perceptron_tagger not found.`,表示`averaged_perceptron_tagger`资源尚未下载到你的机器上
> 
> 在python控制台执行以下代码即可
> ```sh
> import nltk
> nltk.download('averaged_perceptron_tagger')
> ```

> [!NOTE]
> 本项目部分模型使用了深度学习模型，无GPU的设备可能运行缓慢
> 
> 若项目的前后端运行在同一局域网下的不同设备上，请务必关闭设备的防火墙(踩过的坑😂)

## 图片服务
- 本项目使用微软的IIS服务搭建图片服务器，向前端提供图片传输支持
- 即通过IIS服务共享图片，前端可通过HTTP协议直接获取图片数据
- Windows10启动IIS服务器的教程详见[利用windows服务器自带的IIS搭建网站并发布公网访问【内网穿透】](https://developer.aliyun.com/article/1448368)
> [!NOTE]
> 图片数据集来自[Yelp Open Dataset](https://www.yelp.com/dataset)
> 
> 可根据需要自行下载(较为缓慢)，也可通过Issue从开发者处获取
> 
> 注意IIS服务权限设置问题

# 🧰 算法模型
> 点评推荐
<img height="500px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/cba2e3e8-8ead-490c-9cff-5f86aa8dd834"/>

> 好友推荐
<img height="500px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/a2c4685b-af69-46ac-86c4-0e8fda7ca53d"/>

> 经营建议
<img height="500px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/22625d5f-555d-4eea-949b-f125e4e98d1c"/>

# 💻 运行截图
> 项目首页

![首页](https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/103497254/87f05c3c-fd15-45ec-95d6-5571ac297ee3)

> [!NOTE]
> 用户端唯一指定用户名`Shari`，密码任意；商家端唯一指定用户名`asdf`，密码任意
> 
> 别问为什么，问就是项目演示需要😅，登录模块不是本项目的重点
>
> 如果还是想要使用其它用户名，可自行修改login.py中的映射字典

> 数据可视化

<table>
    <tr>
        <td align="center">商户分析</td>
        <td align="center">用户分析</td>
        <td align="center">评论分析</td>
        <td align="center">评分分析</td>
        <td align="center">打卡分析</td>
    </tr>
    <tr>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/1def87ac-3fcd-4da2-8710-01336098e87b"></td>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/65b6ff85-fdcc-444c-8b73-7eb62a38381d"></td>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/611e2552-f661-4926-8c3c-3d180b556a13"></td>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/b2748536-b8dc-4b3a-945d-95db0632b730"></td>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/a0fed411-1d6d-4fcc-8239-4e12cf69aecb"></td>
    </tr>
</table>

> 商户详情&评论情感分析

![商家详情](https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/103497254/4765b133-6328-4446-912b-fc27b015deb2)

> 用户端推荐

<table>
    <tr>
        <td align="center">商户推荐</td>
        <td align="center">好友推荐</td>
    </tr>
    <tr>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/629e1db3-7b61-4c5d-bd63-ce429684f6dc"></td>
         <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/ad97e875-6336-43f5-8c35-538ffe74e29f"></td>
    </tr>
</table>

> [!Important]
> 由于yelp官方开源[数据集](https://www.yelp.com/dataset)中商户数据与图片数据并不完全对应，因此商户卡片的图像为随机选取

> 搜索与筛选

![搜索与筛选](https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/103497254/bd68aa4f-2018-4d8c-a038-a559df1b1b07)

> 商家端

<table>
    <tr>
        <td align="center">商户仪表板</td>
        <td align="center">经营建议</td>
    </tr>
    <tr>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/c608bfcc-0490-471b-af61-0688d2ae8ba3"></td>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/6b3ece34-3561-43a4-be17-5cd56cc2b8b2"></td>
    </tr>
</table>

# 💖 团队成员
本项目由以下四位开发者共同完成(排名不分先后)：[electronic-pig](https://github.com/electronic-pig)、[Labhahaha](https://github.com/Labhahaha)、[zf666fz](https://github.com/zf666fz)、[weeadd](https://github.com/weeadd)

# 📄 写在最后
项目制作不易，如果它对你有帮助的话，请务必给作者点一个免费的⭐，万分感谢!🙏🙏🙏
