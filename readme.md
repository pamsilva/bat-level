# Dummy battery level tracking

Had some issues with my Thinkpad P1 Gen2, where the battery level suddenly dropped to 0% by mistake. Created this to process the logs and visualise the data. The problem seems to be gone ever since I updated the bios version to the latest version available.

## Logging the data

Used this:

```
while true; do echo `date` \| ` upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage ` \
\|  `upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep "time to empty" ` \
\|  `upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep "voltage" ` \
\|  `upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep "energy-rate" ` >> battery-level.data; sleep 15; done
```

To log the battery usage a few more details.

## Visualising the data

Dummy script that uses pandas to load and process the data from a text file into the different cycles; and matplotlib to plot the result. You'll need to edit the script to update any paths that need to match your own system.

![Cycle2](/plots/cycle-2.png)

You can see the battery level dropping to 0% from about 50% around 20h.

![Cycle4](/plots/cycle-4.png)

Haven't seen that happening after upgrading the bios, but I still see random spikes to 100% battery level.
