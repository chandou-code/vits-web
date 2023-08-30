# import schedule
# import time
# import subprocess
#
# count = 0
# def restart_app():
#     print(f'重启{count}')
#     # 停止之前的进程
#     subprocess.call(["taskkill", "/F", "/IM", "python.exe"])
#     print('关闭进程完成')
#     # 启动新的进程
#     subprocess.Popen(["python", "app.py"])
#     print('开启进程完成')
#
#
# # 设定重启时间间隔（每十分钟）
# restart_interval = 1  # 单位：分钟
# schedule.every(restart_interval).minutes.do(restart_app)
#
# while True:
#
#
#     schedule.run_pending()
#     time.sleep(1)


import subprocess
import time
import psutil

def restart_process():
    # 关闭已有进程
    for process in psutil.process_iter():
        if process.name() == 'python.exe' and 'app.py' in process.cmdline():
            process.kill()

    # 打印重启提示
    print('重启中...')

    # 启动新进程
    subprocess.Popen(['python', 'app.py'], shell=True)

while True:
    # 休眠10分钟
    # time.sleep(10 * 60)
    time.sleep(30)
    # 重启进程
    restart_process()
