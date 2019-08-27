"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from KVM import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),#主页
    path('login', views.login),#登录页面
    path('logout', views.logout),#用户登出
    path('kvmVirtual/kvmVirtual.html', views.KvmVirtual),#查看宿主机信息
    path('kvmVirtual/show_active_vhost.html', views.show_active_vhost),#查看已开启的虚拟机
    path('kvmVirtual/show_shut_down.html', views.show_shut_down),#查看已关闭的虚拟机
    path('kvmVirtual/create_Vm_Host.html', views.create_Vm_Host),#创建虚拟机
    path('kvmVirtual/createVmHost', views.createVmHost),
    path('kvmVirtual/create_Vm_Host.html_success', views.create_Vm_Host_success),
    path('kvmVirtual/create_Vm_Host.html_faild', views.create_Vm_Host_faild),
    path('kvmVirtual/lounchVM', views.lounchVm),#启动虚拟机
    path('kvmVirtual/suspendVm', views.suspendVm),#暂停虚拟机
    path('kvmVirtual/resumeVM', views.resumeVM),#暂停虚拟机
    path('kvmVirtual/stopVm', views.stopVm),#关闭虚拟机
    path('kvmVirtual/deleteVm', views.deleteVm),#删除虚拟机
    path('kvmVirtual/configVM', views.configVM),#更改虚拟机配置文件


    #资产管理
    path("CM_entring", views.CM_entring),#资产录入


    # ansible配置文件
    path('ansible_ops/ansible_conf.html', views.ansibleConf),#展示absible配置文件
    path('ansible_ops/ansible_conf_revoke', views.ansible_conf_revoke),#撤销absible配置文件
    path('ansible_ops/ansible_conf', views.ansible_conf),#更改absible配置文件
    path('ansible_ops/ansible_conf_success', views.ansible_conf_success),#确认ansible配置文件修改成功


    #推送配置文件
    path('conf_all/conf_all.html', views.conf_all),#展示推送文件页面
    path('conf_all/conf_all_success', views.conf_all_success),#文件推送


    #nginx_server安装rpm版本nginx
    path('rpm_nginx', views.rpm_nginx),#rpm版本的Nginx安装


    #Nginx启动项
    path('start_Nginx', views.start_Nginx),#启动Nginx
    path('stop_Nginx', views.stop_Nginx),#关闭Nginx
    path('restart_Nginx', views.restart_Nginx),#重启Nginx
    path('enable_Nginx',views.enable_Nginx),#开机自启动Nginx
    path('disable_Nginx',views.disable_Nginx),#开机自启动Nginx


    #apache_server安装rpm版本apache
    path('Apache_Install', views.apache_install),#rpm版本的Apache安装


    #Apache启动项
    path('start_Apache', views.start_Apache),#启动Apache
    path('stop_Apache', views.stop_Apache),#关闭Apache
    path('restart_Apache', views.restart_Apache),#重启Apache
    path('enable_Apache', views.enable_Apache),#开机自启动Apache
    path('disable_Apache', views.disable_Apache),#开机自启动Apache


    #mysql_server安装rpm版本Mysql
    path('Mysql_Install', views.mysql_install),#rpm版本的Apache安装


    #Mysql启动项
    path('start_Mysql', views.start_Mysql),#启动Mysql
    path('stop_Mysql', views.stop_Mysql),#关闭Mysql
    path('restart_Mysql', views.restart_Mysql),#重启Mysql
    path('enable_Mysql', views.enable_Mysql),#开机自启动Mysql
    path('disable_Mysql', views.disable_Mysql),#开机自启动Mysql


    #shell推送器
    path("shell_pull/shellPull.html", views.shell_display),#shell推送器界面展示
    path("shell_pull/shell_pull", views.shell_pull),#shell推送
    path("shell_pull/shellPull_log", views.shell_pull_log),#shell日志


    #LVS_DR安装
    path('LVS_DR/LVS_DR.html', views.LVS_DR_Display),#LVS_DR页面
    path('LVS_DR/LVS_DR_INSTALL', views.LVS_DR_INSTALL),#LVS_DR安装


    #安装zabbix_agent
    path('zabbix_agent_install', views.zabbix_agent),


    #系统任务批量部署
    path('Crontab.html', views.crontab_display),#系统任务表单
    path('CronTab', views.crontab_e),#系统任务部署
]
