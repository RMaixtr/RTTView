
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


# 初始化图表
fig, ax = plt.subplots()
x_data = list(range(1001))
y_data = [0] * 1001
line, = ax.plot([], [], 'r-')

# 设置x轴的界限
ax.set_xlim(0, 1000)
ax.set_ylim(0, 150)

# 初始化图表的数据
def init():
    line.set_data([], [])
    return line,
global_data = b''
# 更新图表的函数
def dataProcess(rcvdbytes):
    global global_data
    try:
        global_data += rcvdbytes
        d = global_data[0:global_data.rfind(b'\r\n')].split(b'\r\n')
        sendlist = []
        for tmp in d:
            if b"gyro_z_rms" in tmp:
                sendlist.append(float(tmp.split()[1].split(b',')[0]))
                print(float(tmp.split()[1].split(b',')[0]))

        for raw_data in sendlist:
            value = float(raw_data)
            y_data.pop(0)
            y_data.append(value)

        line.set_data(x_data, y_data)

        global_data = global_data[global_data.rfind(b'\r\n')+1:]
        return line,
    except Exception as e:
        global_data = b''
        print("Error:", e)
        return line,

# 创建动画
ani = FuncAnimation(fig, dataProcess, frames=np.arange(0, 100), init_func=init, blit=True)

plt.show()
