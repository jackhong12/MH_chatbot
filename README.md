Monster Hunter Guides Chatbot
===
###### tags: `hw` `計算理論`

-------------------------------------------
* File: MHGC 魔物獵人攻略bot
* Author: 黃振宏
* Last updated: 2018/12/18
* Describe:  
    這是魔物獵人世界的攻略查尋器，藉由Chatbot的形式，     你可向Chatbot問最近的活動或者是魔物的資訊
-------------------------------------------

## How to Use
1. 將utils.py中的 ACCESS_TOKEN 後的參數改為 facebook 權杖  
2. 啟動 ngrok  
3. 執行  `$./pyphon3 app.py`  
  
<br>

## File
1. app.py  

2. fsm.py  
    `finite state machine`  
    
3. utils.py   
    `定義回傳facebook的function`  
    
4. monsterHonterCrawler.py   
    `利用 BeautifulSoup module 爬魔物獵人的官網和wiki攻略`   
    `官網: http://game.capcom.com/world/steam/hk/schedule.html`  
    `wiki: https://www.mhchinese.wiki/`  
    
<br>

## Finite State Machine
![](https://i.imgur.com/H2ZzDZx.png)

<br>

## Command
1. `help`
    介紹本Chatbot

2. `video`
    youtube官網宣傳影片
    
3. `本周任務`
    從官網將本周任務的資料爬出來

4. `back`
    返回上步State
    
4. `任務`
    切換到任務查詢State
    a. `任務名`
        顯示任務的圖片和詳細資料

5. `魔物`  
    顯示所有大型和小型魔物  
    > `魔物名稱`
    > 顯示魔物圖片和簡介 
    >> `弱點`
    >> 顯示怪物弱點部位和屬性傷害弱點
    >>
    >> `特徵`
    >> 顯示魔物屬性和咆哮大小等特徵
    >> 
    >> `陷阱`
    >> 顯示各種陷阱對魔物的效果
    >> 
    >> `效果`
    >> 顯示異常屬性對魔物的效果
    
(hint: `指令`: 框框中的為指令)
