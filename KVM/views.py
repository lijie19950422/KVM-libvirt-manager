from django.shortcuts import render
from django.http import HttpResponseRedirect
from KVM.models import KVMUser
from KVM.models import CMDB

import sys
import json

import libvirt
import os
# Create your views here.


def index(request):
    login_success = request.session.get('login_success')
    if login_success:
        data = KVMUser.objects.all()
        username = data[0].username
        cmdb_Vm = CMDB.objects.all().values()
        num = 0
        vm_list = []
        for item in cmdb_Vm:
            vm_list.append(item)
        return render(request, "index.html", {'username': username, 'cmdb_vm': vm_list})
    return render(request, 'login.html', {})

#登录主页
def login(request):
    if request.method == 'POST':
        data = KVMUser.objects.all()
        name = request.POST['username']
        passwd = request.POST['passwd']
        if data[0].username == name and data[0].passwd == passwd:
            request.session["login_success"] = True
            return render(request, 'index.html', {})
        else:
            return render(request, "login.html", {"msg": "用户名密码错误"})
    else:
        return HttpResponseRedirect('/')


#系统登出
def logout(request):
    login_success = request.session.get('login_success')
    if login_success:
        request.session.clear()
        return HttpResponseRedirect('/')


#资产录入
def CM_entring(request):
    login_success = request.session.get('login_success')
    if login_success:
        os.system("rm -rf /tmp/hosts/*")
        os.system("echo > /tmp/host_list")
        os.system("ansible all -m setup --tree /tmp/hosts")
        for file in os.listdir('/tmp/hosts'):
            if os.path.isfile(os.path.join('/tmp/hosts/', file)) == True:
                if file.find('.json') < 0:
                    newname = file + '.json'
                    os.rename(os.path.join('/tmp/hosts/', file), os.path.join('/tmp/hosts', newname))
                else:
                    continue
            else:
                continue
        os.system("ls /tmp/hosts > /tmp/host_list")
        file = open("/tmp/host_list", 'r')
        if file:
            for line in file:
                fact = line.strip('\n')
                file_fact = open("/tmp/hosts/" + fact, "r")
                if file_fact:
                    data = json.loads(file_fact.read())
                    hostname = data['ansible_facts']['ansible_hostname']
                    IP = data['ansible_facts']['ansible_default_ipv4']['address']
                    gateway = data['ansible_facts']['ansible_default_ipv4']['gateway']
                    mac = data['ansible_facts']['ansible_default_ipv4']['macaddress']
                    distribution = data['ansible_facts']['ansible_distribution']
                    distribution_version = data['ansible_facts']['ansible_distribution_version']
                    architecture = data['ansible_facts']['ansible_architecture']
                    kernel = data['ansible_facts']['ansible_kernel']
                    processor = data['ansible_facts']['ansible_processor'][1]
                    processor_cores = data['ansible_facts']['ansible_processor_cores']
                    processor_count = data['ansible_facts']['ansible_processor_count']
                    repeat_ip = CMDB.objects.all().values('IP')
                    if str(repeat_ip) == '<QuerySet []>':
                        CMDB.objects.create(hostname=hostname, IP=IP, gateway=gateway, mac=mac,
                                            distribution=distribution,
                                            distribution_version=distribution_version, architecture=architecture,
                                            kernel=kernel, processor=processor, processor_cores=processor_cores,
                                            processor_count=processor_count)
                    IP_List = []
                    for re_IP in repeat_ip:
                        IP_List.append(re_IP['IP'])
                    if IP in IP_List:
                        pass
                    else:
                        CMDB.objects.create(hostname=hostname, IP=IP, gateway=gateway, mac=mac,
                                            distribution=distribution,
                                            distribution_version=distribution_version, architecture=architecture,
                                            kernel=kernel, processor=processor, processor_cores=processor_cores,
                                            processor_count=processor_count)



                    # for re_IP in repeat_ip:
                    #     if IP == re_IP['IP']:
                    #         pass
                    #     else:
                    #         CMDB.objects.create(hostname=hostname, IP=IP, gateway=gateway, mac=mac, distribution=distribution,
                    #                     distribution_version=distribution_version, architecture=architecture,
                    #                     kernel=kernel, processor=processor, processor_cores=processor_cores,
                    #                     processor_count=processor_count)
                file_fact.close()
        file.close()
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#查看虚拟机信息
def KvmVirtual(request):
    login_success = request.session.get('login_success')
    if login_success:
        conn = libvirt.open("qemu+tcp://127.0.0.1/system")
        data = dict()
        data['info'] = "主机信息"
        hostinfo = conn.getInfo()
        data["平台"] = str(hostinfo[0])
        data["内存"] = str(hostinfo[1]) + "MB"
        data["CPU数量"] = str(hostinfo[2])
        data["类型"] = conn.getType()
        data["地址"] = conn.getURI()
        mem = conn.getFreeMemory()
        data["空闲内存"] = str(mem / 1024 / 1024 / 1024)[0:3] + "GB"
        try:
            conn.close()
        except:
            print("关闭失败！！！")
        print("关闭成功！！！")
        return render(request, "kvmVirtual/kvmVirtual.html", {'data': data})
    return HttpResponseRedirect('/')


#查看已开启的虚拟机
def show_active_vhost(request):
    login_success = request.session.get('login_success')
    if login_success:
        conn = libvirt.open("qemu+tcp://127.0.0.1/system")
        vms_dict = {}
        domain_list = conn.listDomainsID()
        for vm_id in domain_list:
            vms_dict[str(vm_id)] = conn.lookupByID(vm_id).name()
        data = vms_dict
        try:
            conn.close()
        except:
            print("关闭失败！！！")
        print("关闭成功！！！")
        return render(request, "kvmVirtual/show_active_vhost.html", {'data': data})
    return HttpResponseRedirect('/')


#查看已关闭的虚拟机
def show_shut_down(request):
    login_success = request.session.get('login_success')
    if login_success:
        conn = libvirt.open("qemu+tcp://127.0.0.1/system")
        data = conn.listDefinedDomains()
        print("关闭状态虚拟机: %s" % conn.listDefinedDomains())
        try:
            conn.close()
        except:
            print("关闭失败！！！")
        print("关闭成功！！！")
        return render(request, "kvmVirtual/show_shut_down.html", {'data': data})
    return HttpResponseRedirect('/')


#创建虚拟机
def create_Vm_Host(request):
    login_success = request.session.get('login_success')
    if login_success:
        return render(request, "kvmVirtual/create_Vm_Host.html", {})
    return HttpResponseRedirect('/')


def create_Vm_Host_success(request):
    login_success = request.session.get('login_success')
    if login_success:
        return render(request, "kvmVirtual/create_Vm_Host.html", {'msg': '创建成功！'})
    return HttpResponseRedirect('/')


def create_Vm_Host_faild(request):
    login_success = request.session.get('login_success')
    if login_success:
        return render(request, "kvmVirtual/create_Vm_Host.html", {'msg': '创建失败！'})
    return HttpResponseRedirect('/')


def createVmHost(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            Num = int(request.POST['Num'])
            for i in range(Num):
                num = str(i)
                conn = libvirt.open("qemu+tcp://127.0.0.1/system")
                v_host_name = request.POST['vm_hostname'] + '-%s' % num
                os.system(
                    "qemu-img create -f qcow2 -b /var/lib/libvirt/images/centos7.0.qcow2 /var/lib/libvirt/images/%s.qcow2" % v_host_name)
                fo = open("/template/centos7.0.xml", 'r')
                vmConf = fo.read()
                fo.close()
                vmConf = vmConf.replace('centos7.0', v_host_name)
                CPU = request.POST['cpuNum']
                if len(CPU) == 0:
                    CPU = 1
                mem = request.POST['memory']
                if len(mem) == 0:
                    memmory = 1048576
                else:
                    memmory = int(mem) * 1048576

                vmConf = vmConf.replace("<name>centos7.0</name>", "<name>%s</name>" % v_host_name)
                vmConf = vmConf.replace("<source file='/var/lib/libvirt/images/centos7.0.qcow2'/>",
                                        "<source file='/var/lib/libvirt/images/%s.qcow2'/>" % v_host_name)
                vmConf = vmConf.replace("<memory unit='KiB'>1048576</memory>",
                                        "<memory unit='KiB'>%s</memory>" % memmory)
                vmConf = vmConf.replace("<currentMemory unit='KiB'>1048576</currentMemory>",
                                        "<currentMemory unit='KiB'>%s</currentMemory>" % memmory)
                vmConf = vmConf.replace("<vcpu placement='static'>1</vcpu>", "<vcpu placement='static'>%s</vcpu>" % CPU)

                conn.defineXML(vmConf)
                try:
                    conn.close()
                except:
                    print("关闭失败！！！")
            return HttpResponseRedirect('create_Vm_Host.html_success')
        else:
            return HttpResponseRedirect('create_Vm_Host.html_faild')
    return HttpResponseRedirect('/')


#启动虚拟机
def lounchVm(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            conn = libvirt.open("qemu+tcp://127.0.0.1/system")
            vm_hostname = request.POST['lounchVM']
            if vm_hostname in conn.listDefinedDomains():
                vm_host = conn.lookupByName(vm_hostname)
                vm_host.create()
            else:
                return HttpResponseRedirect('show_shut_down.html')
            try:
                conn.close()
            except:
                print("关闭失败！！！")
            print("关闭成功！！！")
            return HttpResponseRedirect('show_shut_down.html')
    return HttpResponseRedirect('/')


#暂停虚拟机
def suspendVm(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            conn = libvirt.open("qemu+tcp://127.0.0.1/system")
            vm_hostname = request.POST['suspendVm']
            if vm_hostname in conn.listDefinedDomains():
                print("虚拟机已关闭，请开启虚拟机后执行")
            else:
                vm_host = conn.lookupByName(vm_hostname)
                vm_host.suspend()
            try:
                conn.close()
            except:
                print("关闭失败！！！")
            print("关闭成功！！！")
            return HttpResponseRedirect('show_active_vhost.html')
    return HttpResponseRedirect('/')



#恢复虚拟机
def resumeVM(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            conn = libvirt.open("qemu+tcp://127.0.0.1/system")
            vm_hostname = request.POST['resumeVM']
            vm_host = conn.lookupByName(vm_hostname)
            vm_host.resume()
            try:
                conn.close()
            except:
                print("关闭失败！！！")
            print("关闭成功！！！")
            return HttpResponseRedirect('show_active_vhost.html')
    return HttpResponseRedirect('/')


#关闭虚拟机
def stopVm(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            conn = libvirt.open("qemu+tcp://127.0.0.1/system")
            vm_hostname = request.POST['stopVm']
            if vm_hostname in conn.listDefinedDomains():
                print("虚拟机已关闭，请开启虚拟机后执行")
            else:
                vm_host = conn.lookupByName(vm_hostname)
                vm_host.destroy()
            try:
                conn.close()
            except:
                print("关闭失败！！！")
            print("关闭成功！！！")
            return HttpResponseRedirect('show_active_vhost.html')
    return HttpResponseRedirect('/')


#删除虚拟机

def deleteVm(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            conn = libvirt.open("qemu+tcp://127.0.0.1/system")
            vm_hostname = request.POST['deleteVm']
            CMDB.objects.filter(hostname='%s' % vm_hostname).delete()
            affirm = 'y'
            if affirm == 'y':
                vm_host = conn.lookupByName(vm_hostname)
                vm_host.undefine()
                os.system("rm -rf /var/lib/libvirt/images/%s.qcow2" % vm_hostname)
            else:
                pass
            try:
                conn.close()
            except:
                print("KVM虚拟机关闭失败！！！")
            print("KVM虚拟机关闭成功！！！")
            return HttpResponseRedirect('show_shut_down.html')
    return HttpResponseRedirect('/')

#配置虚拟机
def configVM(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            vm_hostname = request.POST['vm_hostname']
            os.system("guestmount -a /var/lib/libvirt/images/%s.qcow2 -i /mnt/" % vm_hostname)
            # 增加域名解析
            ip = request.POST['ip']
            domain_name = request.POST['domain_name']
            fo = open("/mnt/etc/hosts", 'a')
            fo.write(ip + "  " + domain_name + "\n")
            fo.close()
            # 修改主机名称：
            new_vm_hostname = request.POST['new_vm_hostname']
            fo = open("/mnt/etc/hostname", "w")
            fo.write(new_vm_hostname)
            fo.close()
            # 修改IP地址
            new_ip = request.POST['new_ip']
            new_ip_data = 'IPADDR=' + str(new_ip)
            ip_conf = [
                'ONBOOT=yes', '\n',
                'NETBOOT=yes', '\n',
                'IPV6INIT=yes', '\n',
                'BOOTPROTO=static', '\n',
                'TYPE=Ethernet', '\n',
                'PREFIX=24', '\n',
                'GATEWAY=192.168.122.1', '\n',
                'DNS1=202.207.48.3', '\n',
                'DNS2=114.114.114.114',
                '\n']
            ip_conf.append(new_ip_data)
            fo = open("/mnt/etc/sysconfig/network-scripts/ifcfg-eth0", "w")
            fo.writelines(ip_conf)
            fo.close()
            os.system("umount /mnt")
            return HttpResponseRedirect('show_shut_down.html')
    return HttpResponseRedirect('/')


#rpm版Nginx安装
def rpm_nginx(request):
    login_success = request.session.get('login_success')
    if login_success:
        nginx_yum = "ansible nginx_server -m shell -a 'yum clean all'"
        os.system(nginx_yum)
        nginx_yum_repo = "ansible nginx_server -m shell -a 'yum repolist'"
        os.system(nginx_yum_repo)
        epel_release = "ansible nginx_server -m shell -a 'yum install -y epel-release'"
        os.system(epel_release)
        nginx_install = "ansible nginx_server -m yum -a 'name=nginx state=present'"
        os.system(nginx_install)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#启动Nginx(rpm)
def start_Nginx(request):
    login_success = request.session.get('login_success')
    if login_success:
        startNginx = "ansible nginx_server -m shell -a 'systemctl start nginx'"
        os.system(startNginx)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#关闭Nginx(rpm)
def stop_Nginx(request):
    login_success = request.session.get('login_success')
    if login_success:
        stopNginx = "ansible nginx_server -m shell -a 'systemctl stop nginx'"
        os.system(stopNginx)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#重启Nginx(rpm)
def restart_Nginx(request):
    login_success = request.session.get('login_success')
    if login_success:
        restartNginx = "ansible nginx_server -m shell -a 'systemctl restart nginx'"
        os.system(restartNginx)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#开机自启动Nginx(rpm)
def enable_Nginx(request):
    login_success = request.session.get('login_success')
    if login_success:
        enableNginx = "ansible nginx_server -m shell -a 'systemctl enable nginx'"
        os.system(enableNginx)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')



#开机不启动Nginx(rpm)
def disable_Nginx(request):
    login_success = request.session.get('login_success')
    if login_success:
        disableNginx = "ansible nginx_server -m shell -a 'systemctl disable nginx'"
        os.system(disableNginx)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

#Apache安装
def apache_install(request):
    login_success = request.session.get('login_success')
    if login_success:
        apaInstall = "ansible apache_server -m yum -a 'name=httpd state=present'"
        os.system(apaInstall)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#启动Nginx(rpm)
def start_Apache(request):
    login_success = request.session.get('login_success')
    if login_success:
        startApache = "ansible apache_server -m shell -a 'systemctl start httpd'"
        os.system(startApache)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#关闭Apache
def stop_Apache(request):
    login_success = request.session.get('login_success')
    if login_success:
        stopApache = "ansible apache_server -m shell -a 'systemctl stop httpd'"
        os.system(stopApache)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#重启Apache(rpm)
def restart_Apache(request):
    login_success = request.session.get('login_success')
    if login_success:
        restartApache = "ansible apache_server -m shell -a 'systemctl restart httpd'"
        os.system(restartApache)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#开机自启动Apache
def enable_Apache(request):
    login_success = request.session.get('login_success')
    if login_success:
        enableApache = "ansible apache_server -m shell -a 'systemctl enable httpd'"
        os.system(enableApache)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#开机不启动Apache
def disable_Apache(request):
    login_success = request.session.get('login_success')
    if login_success:
        disableApache = "ansible apache_server -m shell -a 'systemctl disable httpd'"
        os.system(disableApache)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#Mysql安装
def mysql_install(request):
    login_success = request.session.get('login_success')
    if login_success:
        wget_install = "ansible mysql_server -m yum -a 'name=wget state=present'"
        os.system(wget_install)
        # yumData = "ansible mysql_server -m shell -a 'wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo'"
        # os.system(yumData)
        # yumCache = "ansible mysql_server -m shell -a 'yum clean all && yum repolist'"
        # os.system(yumCache)
        # epel_release = "ansible mysql_server -m shell -a 'yum install -y epel-release'"
        # os.system(epel_release)
        rpm_mysql = "ansible mysql_server -m shell -a 'wget http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm'"
        os.system(rpm_mysql)
        localInstall = "ansible mysql_server -m shell -a 'yum localinstall  -y mysql57-community-release-el7-8.noarch.rpm'"
        os.system(localInstall)
        mysqlInstall = "ansible mysql_server -m shell -a 'yum install -y mysql mysql-server mysql-devel'"
        os.system(mysqlInstall)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#启动Mysql(rpm)
def start_Mysql(request):
    login_success = request.session.get('login_success')
    if login_success:
        startMysql = "ansible mysql_server -m shell -a 'systemctl start mysqld'"
        os.system(startMysql)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#关闭Mysql
def stop_Mysql(request):
    login_success = request.session.get('login_success')
    if login_success:
        stopMysql = "ansible mysql_server -m shell -a 'systemctl stop mysqld'"
        os.system(stopMysql)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#重启Mysql(rpm)
def restart_Mysql(request):
    login_success = request.session.get('login_success')
    if login_success:
        restartMysql = "ansible mysql_server -m shell -a 'systemctl restart mysqld'"
        os.system(restartMysql)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#开机自启动Mysql
def enable_Mysql(request):
    login_success = request.session.get('login_success')
    if login_success:
        enableMysql = "ansible mysql_server -m shell -a 'systemctl enable mysqld'"
        os.system(enableMysql)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#开机不启动Mysql
def disable_Mysql(request):
    login_success = request.session.get('login_success')
    if login_success:
        disableMysql = "ansible mysql_server -m shell -a 'systemctl disable mysqld'"
        os.system(disableMysql)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#展示ansible配置文件
def ansibleConf(request):
    login_success = request.session.get('login_success')
    if login_success:
        with open("/etc/ansible/hosts", "r") as fo:
            data = fo.read()
        return render(request, "ansible_ops/ansible_conf.html", {"ansible_conf": data})
    return HttpResponseRedirect('/')


#撤销ansible配置文件
def ansible_conf_revoke(request):
    login_success = request.session.get('login_success')
    if login_success:
        with open("/etc/ansible/hosts", "r") as fo:
            data = fo.read()
        return render(request, "ansible_ops/ansible_conf.html", {"ansible_conf": data})
    return HttpResponseRedirect('/')


#更改配置文件
def ansible_conf(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            data = request.POST['ansibleConf']
            with open("/etc/ansible/hosts", "w") as fo:
                fo.write(str(data))
            return HttpResponseRedirect('ansible_conf_success', )
    return HttpResponseRedirect('/')


#确认ansible配置文件修改成功
def ansible_conf_success(request):
    login_success = request.session.get('login_success')
    if login_success:
        with open("/etc/ansible/hosts", "r") as fo:
            data = fo.read()
        return render(request, "ansible_ops/ansible_conf.html", {"ansible_conf": data, 'conf_msg': '修改已生效'})
    return HttpResponseRedirect('/')


#批量推送配置文件
def conf_all(request):
    login_success = request.session.get('login_success')
    if login_success:
        return render(request, "conf_all/conf_all.html", {})
    return HttpResponseRedirect('/')


def conf_all_success(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            ip_server = str(request.POST['ip_server'])
            src_file = str(request.POST['src_file'])
            dest_file = str(request.POST['dest_file'])
            conf_all = "ansible %s -m copy -a 'src=%s dest=%s'" % (ip_server, src_file, dest_file)
            os.system(conf_all)
            return HttpResponseRedirect("conf_all.html")
    return HttpResponseRedirect('/')


#shell脚本推送器
def shell_display(request):
    login_success = request.session.get('login_success')
    if login_success:
        return render(request, "shell_pull/shellPull.html", {})
    return HttpResponseRedirect('/')


def shell_pull(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            ip_group = str(request.POST['ip_group'])
            code = str(request.POST['shell_pull_code'])
            shell_code = "ansible %s -m shell -a '%s'" % (ip_group, code)
            os.system(shell_code + "> /tmp/shell_log.txt")
            return HttpResponseRedirect("shellPull_log")
        return HttpResponseRedirect('/')


#shell脚本执行日志
def shell_pull_log(request):
    login_success = request.session.get('login_success')
    if login_success:
        with open("/tmp/shell_log.txt", "r") as fo:
            shell_log = fo.read()
        return render(request, "shell_pull/shellPull.html", {'shell_log': shell_log})
    return HttpResponseRedirect('/')


#LVS_DR 展示
def LVS_DR_Display(request):
    login_success = request.session.get('login_success')
    if login_success:
        return render(request, "LVS_DR/LVS_DR.html", {})
    return HttpResponseRedirect('/')


#LVS_DR 集群部署
def LVS_DR_INSTALL(request):
    login_success = request.session.get('login_success')
    if login_success:
        if request.method == 'POST':
            # 开启路由转发
            IP_FORWARD = "ansible LVS_DR_server -m shell -a 'echo 1 > /proc/sys/net/ipv4/ip_forward'"
            os.system(IP_FORWARD)
            # 设置虚拟IP
            VIP = str(request.POST['VIP'])
            Virtual_IP = "ansible LVS_DR_server -m shell -a 'ip addr add %s/32 dev lo'" % VIP
            os.system(Virtual_IP)
            #安装LVS
            LVS_Install = "ansible LVS_DR_server -m yum -a'name=ipvsadm state=present'"
            os.system(LVS_Install)
            #配置策略
            policy = str(request.POST['policy'])
            LVS_Port = str(request.POST['LVS_Port'])
            LVS_Policy = "ansible LVS_DR_server -m shell -a'ipvsadm -A -t  %s:%s -s %s'" % (VIP, LVS_Port, policy)
            os.system(LVS_Policy)
            RIP_Server = str(request.POST['RIP_Server'])
            RIP = """ansible %s -m shell -a "ip addr show dev eth0 | sed -n '3p' | awk '{print \$2}'" """ % RIP_Server
            data = os.popen(RIP)
            IP_Read = data.read()
            RIP_data = IP_Read.split('\n')[1::2]
            #分配策略
            RS_Port = str(request.POST['RS_Port'])
            for i in RIP_data:
                rip = i.split('/24')[0]
                distribute_policy = "ansible LVS_DR_server -m shell -a 'ipvsadm -a -t %s:%s -r %s:%s -g'" % (VIP, LVS_Port, rip, RS_Port)
                os.system(distribute_policy)
            #部署RS_Server------增加lo
            RS_Server_lo = "ansible %s -m shell -a 'ip addr add %s/32 dev lo'" % (RIP_Server, VIP)
            os.system(RS_Server_lo)
            #部署RS_Server------闭嘴
            RS_Server_ignore = "ansible %s -m shell -a 'echo 1 > /proc/sys/net/ipv4/conf/eth0/arp_ignore '" % RIP_Server
            os.system(RS_Server_ignore)
            #开启转发数据功能
            RS_Server_announce = "ansible %s -m shell -a 'echo 2 > /proc/sys/net/ipv4/conf/eth0/arp_announce'" % RIP_Server
            os.system(RS_Server_announce)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

#zabbix-agent部署
def zabbix_agent(request):
    login_success = request.session.get('login_success')
    if login_success:
        zabbix_agent_Install1 = "ansible all -m copy -a 'src=/root/Downloads/zabbix-release-4.0-1.el7.noarch.rpm dest=/tmp'"
        os.system(zabbix_agent_Install1)
        zabbix_agent_Install2 = "ansible all -m shell -a 'rpm -ivh /tmp/zabbix-release-4.0-1.el7.noarch.rpm'"
        os.system(zabbix_agent_Install2)
        zabbix_agent_Install3 = "ansible all -m shell -a 'yum install -y zabbix-agent'"
        os.system(zabbix_agent_Install3)
        #删除旧的配置文件
        rm_conf = "ansible all -m shell -a ' rm -rf /etc/zabbix/zabbix_agentd.conf'"
        os.system(rm_conf)
        #更改zabbix-agent配置
        update_zabbix_agent = "ansible all -m copy -a 'src=/zabbix/zabbix_agentd.conf dest=/etc/zabbix/ '"
        os.system(update_zabbix_agent)
        #启动zabbix-agent
        start_agent = "ansible all -m shell -a 'systemctl start zabbix-agent && systemctl enable zabbix-agent'"
        os.system(start_agent)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


#展示系统任务表单
def crontab_display(request):
    login_success = request.session.get('login_success')
    if login_success:
        return render(request, "Crontab.html", {})
    return HttpResponseRedirect('/')


#批量部署系统定时任务
def crontab_e(request):
    login_success = request.session.get('login_success')
    if login_success:
        server_groups = str(request.POST['server_groups'])
        minute = str(request.POST['minute'])
        hour = str(request.POST['hour'])
        day = str(request.POST['day'])
        month = str(request.POST['month'])
        weekday = str(request.POST['weekday'])
        name = str(request.POST['cron_name'])
        job = str(request.POST['job'])
        state = str(request.POST['state'])
        print(state,server_groups,minute,hour,day,month,weekday,name,job)
        crontab = """ansible %s -m cron -a 'minute=%s hour=%s day=%s month=%s weekday=%s name="%s"  job="%s" state=%s'""" % (server_groups,
                                                                                                                       minute, hour, day,
                                                                                                                          month, weekday,
                                                                                                                          name, job, state)
        print(crontab)
        os.system(crontab)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

