import matplotlib.pyplot as plt
import argparse
import subprocess
import re
import matplotlib.animation as animation
from datetime import datetime

airport_tool_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
logfile = "rssi.log"


def get_rssi():

    data = subprocess.check_output([airport_tool_path, '-I'])
    data = data.decode()
  

    m = re.search(r"agrCtlRSSI: [-+]\d+", data)
    rssi = int(m.group(0).split(":")[1])
    m = re.search(r"agrCtlNoise: [-+]\d+", data)
    rssi_noise = int(m.group(0).split(":")[1])
    return rssi, rssi_noise

def update(frame):
    #print(frame)

    
    delta_t = (datetime.now() - t_start).seconds

    t.append(delta_t)
    rssi, noise = get_rssi()
    rssi_data.append(rssi)
    rssi_noise_data.append(noise)
    ax_rssi.plot(t,rssi_data)
    ax_rssi_noise.plot(t, rssi_noise_data)
    
    ax_rssi.set_title("RSSI")
    ax_rssi_noise.set_title("Noise level")
    #ax_rssi.set_xlabel("Time [s]")
    ax_rssi_noise.set_xlabel("Time [s]")
    ax_rssi.set_ylabel("dB")
    ax_rssi_noise.set_ylabel("dB")
    
    with open(logfile,"a+") as f:
        f.write("0, " + str(rssi) + ", " + str(noise) + "\n")
    
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", help="Show GUI plot", action='store_true')

    args = parser.parse_args()

    rssi, noise = get_rssi()
    with open(logfile,"w") as f:
        f.write("# time[s], rssi[db], noise[db]\n")
        f.write("0, " + str(rssi) + ", " + str(noise) + "\n")
        
        #logfile"# time[s], rssi[db], noise[db]")
        
        #print( rssi,noise)



    if args.gui:
    
        fig, [ax_rssi, ax_rssi_noise] = plt.subplots(2,1)
        fig.set_size_inches(10,8)
        ax_rssi.plot([])
        ax_rssi_noise.plot([])
        rssi_data = []
        rssi_noise_data = []
        t = [0]
        t_start = datetime.now()

        
        rssi_data.append(rssi)
        rssi_noise_data.append(noise)
        ax_rssi.plot(t, rssi_data)
        ax_rssi_noise.plot(t, rssi_noise_data)


        animation = animation.FuncAnimation(fig, update, frames=get_rssi(), interval=200)
        plt.show()


    

