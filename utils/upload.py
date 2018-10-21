# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
import paramiko


def sftp_upload_file(host, user, password, server_path, local_path):
    ret = {'status': 0}
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
    except Exception as e:
        ret['status'] = 1
        ret['msg'] = '连接不成功，上传失败 %s' % e
    return ret