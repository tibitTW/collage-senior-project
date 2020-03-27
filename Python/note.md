# Note

- 馬達參數
    1 mm/min = 2/3 pps
    PLC -> D10
- 送線速度
    PLC -> D12
- 電壓電流
    PLC -> D100/D200: 0~4000

- 手動模式
    PLC -> S4
  - 走台 PLC -> X13
- 自動模式
    PLC -> S5

- 焊接開始
    PLC -> M500

- python script autostart
    1. ~/etc/rc.local
    2. ~/.profile
    3. ~/.config/lxsession/LXDE-pi/autostart
    4. ~/.bashrc
