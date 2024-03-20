<div align="center">
    <p align="center">
        <img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/c430bbf2-fa74-4235-b078-0f4b7b571353" alt="logo" width="500" />
    </p>
    
![GitHub License](https://img.shields.io/github/license/electronic-pig/Yelp-Analysis-and-Reco_frontend)
![Static Badge](https://img.shields.io/badge/contributors-4-lightblue)
![GitHub Repo stars](https://img.shields.io/github/stars/electronic-pig/Yelp-Analysis-and-Reco_frontend)

<h2 align="center">Yelp-Analysis-and-Reco</h2>
</div>

# ✨ 简介

这是yelp点评数据分析与推荐项目的后端仓库，是集成了大数据分析及可视化，以及大数据应用开发的WebApp应用.

前端仓库请移步[Yelp-Analysis-and-Reco_frontend](https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend)

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

- Flask
- Pytorch
- Scikit-learn + Scikit-suprise
<a title="flask" href="https://flask.palletsprojects.com/">
    <img height="100px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/3cd27a4b-7268-401a-afc9-ea9a118caa31"/>
</a>
<a title="pytorch" href="https://pytorch.org">
    <img height="100px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/56c66fc1-0491-4eae-bad5-4c08115c4776"/>
</a>
<a title="scikit-learn" href="https://scikit-learn.org/stable/index.html">
    <img height="100px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/18254205-d00a-4f99-aa85-5e3d1dfbf1ab"/>
</a>



# 🚀 项目运行说明

## 安装依赖
```sh
pip intsall requriement.txt
```

## 编译运行
- 在`main.js`中填写你的BaiduMap_api_key
- 在`.env.development`中填写你的后端服务地址
```sh
npm run dev
```

## 打包部署(可选)
- 在`.env.production`中填写你的后端服务地址
```sh
npm run build
```
> [!NOTE]
> 若项目的前后端运行在同一局域网下的不同设备上，请务必关闭设备的防火墙(踩过的坑😂)

# 💻 运行截图
> 项目首页

![首页](https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/28c9ad69-ae7c-49ce-b4da-c761a6a77218)

> [!NOTE]
> 用户端唯一指定用户名`Shari`，密码任意；商家端唯一指定用户名`asdf`，密码任意
> 
> 别问为什么，问就是项目演示需要😅，登录模块不是本项目的重点

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

![商家详情](https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/0fd859cc-039c-4ee6-a641-05644e821f80)

> 用户端推荐、搜索

<table>
    <tr>
        <td align="center">商户推荐</td>
        <td align="center">用户搜索</td>
        <td align="center">好友推荐</td>
    </tr>
    <tr>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/629e1db3-7b61-4c5d-bd63-ce429684f6dc"></td>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/285b83a8-3f9d-4724-bfbf-9b64804835c6"></td>
        <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/ad97e875-6336-43f5-8c35-538ffe74e29f"></td>
    </tr>
</table>

> [!Important]
> 由于yelp官方开源[数据集](https://www.yelp.com/dataset)中商户数据与图片数据并不完全对应，因此商户卡片的图像为随机选取

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
项目制作不易，如果它对你有帮助的话，请务必给作者点一个免费的⭐，万分感谢!🙏
