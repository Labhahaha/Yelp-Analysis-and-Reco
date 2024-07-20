An English version of the README for this project:

------

<div align="center">     <p align="center">         <img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/c430bbf2-fa74-4235-b078-0f4b7b571353" alt="logo" width="500" />     </p>

![GitHub License](https://img.shields.io/github/license/Labhahaha/Yelp-Analysis-and-Reco) ![Collaborators](https://img.shields.io/badge/collaborator-4-lightblue) ![Python Version](https://img.shields.io/badge/python-3.7-orange.svg) ![GitHub Repo Stars](https://img.shields.io/github/stars/Labhahaha/Yelp-Analysis-and-Reco)

<h2 align="center">Yelp-Analysis-and-Reco</h2> </div>

# ✨ Introduction

This is the backend repository for the Yelp review data analysis and recommendation project, which integrates collaborative filtering recommendation algorithms, search algorithms, and NLP sentiment analysis algorithms into a Flask backend application.

For the frontend repository, please visit [Yelp-Analysis-and-Reco_frontend](https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend).

# 🎉 Features

## Data Visualization

- Business Analysis
- User Analysis
- Review Analysis
- Rating Analysis
- Check-in Analysis

## Application Functions

- User Review Recommendations
- User Business Search
- User Friend Recommendations
- Business Operational Recommendations
- Review Sentiment Analysis

> [!Warning]
> The icons and homepage images used in this project are from the [official Yelp website](https://www.yelp.com/). This open-source project is for learning and communication purposes only. Please comply with relevant copyright regulations.

# 🛠 Tech Stack

| [Flask](https://flask.palletsprojects.com/) | [PyTorch](https://pytorch.org) | [Scikit-learn](https://scikit-learn.org/stable/index.html) | [Scikit-surprise](https://surpriselib.com/) |
| ------------------------------------------- | ------------------------------ | ---------------------------------------------------------- | ------------------------------------------- |
| [](https://flask.palletsprojects.com/)      | [](https://pytorch.org)        | [](https://scikit-learn.org/stable/index.html)             | [](https://surpriselib.com/)                |

# 🚀 Getting Started

## Install Dependencies

```
pip install -r requirements.txt
```

> [!NOTE]
> Ensure the PyTorch version matches the CUDA version of your device's GPU.

## Project Setup

- Fill in your database server address and port in `config/config.py`.
- Fill in your API_TOKEN for Baidu Wenxin in `app/Advice/Boards.py`.
- Place your model weight files in `config/model`.

> [!NOTE]
> The project's database is based on the [Yelp open dataset](https://www.yelp.com/dataset) with additional processing and filtering, and several new tables added.
>
> The database and pre-trained model weights used in the project can be obtained from the developers via Issues, or you can process and train them yourself.

## Run the Project

```
python run.py
```

> [!Warning]
> If you encounter the error `Resource averaged_perceptron_tagger not found.`, it means the `averaged_perceptron_tagger` resource has not been downloaded to your machine.
>
> Run the following code in the Python console to resolve it:
>
> ```
> import nltk
> nltk.download('averaged_perceptron_tagger')
> ```

> [!NOTE]
> Some models used in this project are deep learning models, which may run slowly on devices without a GPU.
>
> If the project's frontend and backend are running on different devices in the same local network, make sure to disable the firewall on the devices (lessons learned 😅).

## Image Service

- This project uses Microsoft's IIS service to set up an image server, providing image transmission support to the frontend.
- By sharing images through the IIS service, the frontend can directly access image data via the HTTP protocol.
- For a tutorial on setting up an IIS server on Windows 10, refer to [Using Windows Server's Built-in IIS to Set Up a Website and Publish it for Public Access (Intranet Penetration)](https://developer.aliyun.com/article/1448368).

> [!NOTE]
> The image dataset is from the [Yelp Open Dataset](https://www.yelp.com/dataset).
>
> You can download it yourself (it may be slow), or obtain it from the developers via Issues.
>
> Be mindful of the IIS service permission settings.

# 🧰 Algorithm Models

> Review Recommendations <img height="500px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/cba2e3e8-8ead-490c-9cff-5f86aa8dd834"/>

> Friend Recommendations <img height="500px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/a2c4685b-af69-46ac-86c4-0e8fda7ca53d"/>

> Business Advice <img height="500px" src="https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/95296826/22625d5f-555d-4eea-949b-f125e4e98d1c"/>

# 💻 Screenshots

> Project Homepage

![Homepage](https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/103497254/87f05c3c-fd15-45ec-95d6-5571ac297ee3)

> [!NOTE]
> The only specified username for the user end is **Shari**, with any password; the only specified username for the business end is **asdf**, with any password.
>
> Don't ask why 😅. It's for project demonstration purposes, and the login module is not the focus of this project.
>
> If you still want to use other usernames, you can modify the mapping dictionary in `login.py`.

> Data Visualization

<table>     <tr>         <td align="center">Business Analysis</td>         <td align="center">User Analysis</td>         <td align="center">Review Analysis</td>         <td align="center">Rating Analysis</td>         <td align="center">Check-in Analysis</td>     </tr>     <tr>         <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/1def87ac-3fcd-4da2-8710-01336098e87b"></td>         <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/65b6ff85-fdcc-444c-8b73-7eb62a38381d"></td>         <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/611e2552-f661-4926-8c3c-3d180b556a13"></td>         <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/b2748536-b8dc-4b3a-945d-95db0632b730"></td>         <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/a0fed411-1d6d-4fcc-8239-4e12cf69aecb"></td>     </tr> </table>

> Business Details & Review Sentiment Analysis

![Business Details](https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/103497254/4765b133-6328-4446-912b-fc27b015deb2)

> User End Recommendations

<table>     <tr>         <td align="center">Business Recommendations</td>         <td align="center">Friend Recommendations</td>     </tr>     <tr>         <td><img src="https://github.com/electronic-pig/Y

elp-Analysis-and-Reco_frontend/assets/103497254/629e1db3-7b61-4c5d-bd63-ce429684f6dc"></td> <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/ad97e875-6336-43f5-8c35-538ffe74e29f"></td> </tr>

</table>

> [!Important]
>  Because the business data in the Yelp open [dataset](https://www.yelp.com/dataset) does not completely match the image data, the images for the business cards are randomly selected.

> Search and Filter

![Search and Filter](https://github.com/Labhahaha/Yelp-Analysis-and-Reco/assets/103497254/bd68aa4f-2018-4d8c-a038-a559df1b1b07)

> Business End

<table>     <tr>         <td align="center">Business Dashboard</td>         <td align="center">Operational Advice</td>     </tr>     <tr>         <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/c608bfcc-0490-471b-af61-0688d2ae8ba3"></td>         <td><img src="https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend/assets/103497254/6b3ece34-3561-43a4-be17-5cd56cc2b8b2"></td>     </tr> </table>

# 💖 Team Members

This project was collaboratively developed by the following developers (in no particular order): [electronic-pig](https://github.com/electronic-pig), [Labhahaha](https://github.com/Labhahaha), [zf666fz](https://github.com/zf666fz), [weeadd](https://github.com/weeadd).

# 📄 Conclusion

Developing this project was not easy. If it has helped you, please give the author a free ⭐. Thank you very much! 🙏🙏🙏
