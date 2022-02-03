# 🪐Milimate_Back🪐

## 🪐팀원 소개




## 🪐개발 아키텍처
![img/architecture.png](img/architecture.png)

## 🪐기술 스택

|         |                           |
|---------|---------------------------|
| **인프라** | Docker, Github action     |
| **언어**  | Python                    |
| **프레임워크** | Django 3.1.14             |
| **데이터베이스** | MySQL, RDS, S3            |
| **웹 서버** | EC2, Nginx, gunicorn, Django |


## 🪐폴더 구조
```
MyPlanIt_Back
│
└───accounts(앱)
└───plan(앱)
└───todo(앱)
│
└───myplanit(프로젝트)
│   │   __init__.py
│   │   asgi.py
│   │   urls.py
│   │   wsgi.py
│   │
│   └───settings
│           __init__.py
│           base.py
│           dev.py
│           prod.py
│
└───config
│   │
│   └───docker
│   │       entrypoint.prod.sh
│   │
│   └───nginx
│   │       Dockerfile
│   │       nginx.conf
│   │
│   └───scripts
│           deploy.sh
│
└───docker-compose.prod.yml
└───docker-compose.yml
└───Dockerfile
└───Dockerfile.prod
└───manage.py
└───README.md
└───requirements.txt

```


## 🪐API 명세서
[API명세서 자세히보기](https://documenter.getpostman.com/view/17888573/UVXkmZke)




## 🪐팀원 역할분담
![img/role.png](img/role.png)


## 🪐ERD
![img/erd.png](img/erd.png)

## 🪐어려웠던 점 / 해결한 점


## 🪐회고