# Inputs and Outputs from Database

'''
VERDE
0. Edge Node -> Server: copyUsers() || Ariana y Julio
NEGRO
1. Edge Node -> Server: askQRAndActivate(string url) || Ariana y Julio
NARANJA
2. Mobile -> Server: utilizeQR(string uuid) || Lucero y Ariana
   1. Server -> EdgeNode: requestOpening() || Ariana y Julio
   2. EdgeNode -> ESP32 Entry: requestImage() || Ariana y Eric
   3. EdgeNode -> ESP32 Entry: open() || Ariana y Eric
RED
3. ESP32 Exit -> Edge Node: requestOpening() || Luis y Julio
AZUL
4. ESP32 Screen -> Edge Node: getQR() || Lucero y Julio
'''