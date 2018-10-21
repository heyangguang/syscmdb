# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
import paramiko


def sftp_exec_command(host, port, user, password, command):
    ret = {'status': 0}
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port, user, password)
        try:
            std_in, std_out, std_err = ssh_client.exec_command(command)
        except Exception as e:
            ret['status'] = 1
            ret['msg'] = '执行失败,执行失败 %s' % e
            ssh_client.close()
    except Exception as e:
        ret['status'] = 1
        ret['msg'] = '环境错误,执行失败 %s' % e
    return ret
