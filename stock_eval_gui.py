import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import twstock
import os

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'}

# 營收變化
def rev_trend():   # GUI用的函式袂使佇()內底寫參數。
    global stk
    stk=entry.get()
    form_data={
               'encodeURIComponent':'1',
               'step':'1',
               'firstin':'1',
               'off':'1',
               'keyword4':'',
               'code1':'',
               'TYPEK2':'',
               'checkbtn':'',
               'queryName':'co_id',
               'inpuType':'co_id',
               'TYPEK':'all',
               'isnew':'true',
               'co_id':stk,
               'year':'',
               'month':''
    }

    
    resp = requests.post('https://mops.twse.com.tw/mops/web/t05st10_ifrs', form_data, headers=headers)
    resp.encoding='utf-8'
    soup=BeautifulSoup(resp.text,'lxml')
    
    
    global directory_path
    
    directory_path=filedialog.askdirectory()
    
    if directory_path:
         
        file_path=os.path.join(directory_path, f"{stk}評估報告.txt")
    
    with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f'{stk}評估報告\n\n一、營收情況(袂使減超過25%）\n')

    try:
        labelVar.set('開始檢查'+stk+'...')
        t=soup.find('table',class_="hasBorder").find_all('tr')
        # 月營收年增率
        mm=float(t[4].find('td').text.strip())
        # 共總營收年增率
        yy=float(t[8].find('td').text.strip())
        
        if mm<-25 and yy<-25:
            labelVar.set(stk+'月營收比舊年的變化是'+str(mm)+'%，\n共總年營收比舊年的變化是'+str(yy)+'%。\n'+stk+'營收有真大的衰退，無閣考慮！\n（已經寫入去評估報告！）')
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(stk+'月營收比舊年的變化是'+str(mm)+'%，\n共總年營收比舊年的變化是'+str(yy)+'%。\n'+stk+'營收有真大的衰退，無閣考慮！\n\n')
        else:
            labelVar.set(stk+'月營收比舊年的變化是'+str(mm)+'%，\n共總年營收比舊年的變化是'+str(yy)+'%。\n'+stk+'營收表現無問題！\n（已經寫入去評估報告！）')
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(stk+'月營收比舊年的變化是'+str(mm)+'%，\n共總年營收比舊年的變化是'+str(yy)+'%。\n'+stk+'營收表現無問題！\n\n')
    except:
        labelVar.set(stk+'營收評估過程發生錯誤！。\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
                f.write(stk+'營收評估過程發生錯誤！請另外閣評估。\n\n')
    finally:
        if tk.messagebox.askquestion(title='訊息', message='敢欲繼續評估別个項目？')=='yes':
            cash_divs()
        else:
            root.destroy()

# 五年殖利率

def cash_divs():
    global stk
    stk=entry.get()
    r = requests.get('https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID='+str(stk),headers=headers)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')
    table=soup.find('table',id='tblDetail')
    
    file_path=os.path.join(directory_path, f"{stk}評估報告.txt")
    with open(file_path, 'a', encoding='utf-8') as f:
            f.write('二、現金股利分發(上無愛有5%）\n')

    tr_qual=[]
    try:
        for tr in table.find_all('tr'):
            if tr.find_all('td')!=[] and '∟'!=tr.find_all('td')[0].text.strip():
                tr_qual.append(tr)
    except:
        labelVar.set(f'{stk}的殖利率評估出現錯誤，請另外檢查！\n')

    cdr=[]
    pcr=[]

    for y in tr_qual[0:5]:
        cdr.append(y.find_all('td')[16].text.strip())  # 2023年第五个tr內底第十七个td；後一个tr內底仝款第十七个td
        pcr.append(y.find_all('td')[21].text.strip())
    labelVar.set(f'{stk}過去五冬的現金殖利率是{cdr[0]}%、{cdr[1]}%、{cdr[2]}%、{cdr[3]}%、{cdr[4]}%。\n（已經寫入去評估報告！）')
    labelVar.set(f'{stk}過去五冬的盈餘配息率是{pcr[0]}%、{pcr[1]}%、{pcr[2]}%、{pcr[3]}%、{pcr[4]}%。\n（已經寫入去評估報告！）')
    with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}過去五冬的現金殖利率是{cdr[0]}%、{cdr[1]}%、{cdr[2]}%、{cdr[3]}%、{cdr[4]}%。\n{stk}過去五冬的盈餘配息率是{pcr[0]}%、{pcr[1]}%、{pcr[2]}%、{pcr[3]}%、{pcr[4]}%。\n')
    
        
    # 檢查過去五冬現金殖利率
    low_cdr=[]
    for j in cdr:
        try:
            if float(j)<5 or j =='-':
                low_cdr.append(j)
            
        except ValueError as e:
            labelVar.set(f'{stk}過去五冬捌無分現金股利。訊息：{e}\n（已經寫入去評估報告！）')
            with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f'{stk}過去五冬捌無分現金股利。訊息：{e}\n')
    if low_cdr==[]:
        labelVar.set(f'{stk}過去五冬殖利率攏較懸5%。\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'{stk}過去五冬殖利率攏較懸5%。\n')
    else:
        labelVar.set(f'{stk}出現過去五冬比5%較減的殖利率：{low_cdr}（%）!\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'{stk}出現過去五冬比5%較減的殖利率：{low_cdr}（%），無閣考慮!\n')

    
    rate = 0
    m=len(pcr)
    for u in pcr:
        try:
            l=float(u)
            rate+=l
        except ValueError:
            m-=1
        finally:
            avg_cr=rate/m
    labelVar.set(f'{stk}過去五冬的平均盈餘配息率是{avg_cr:.2f}%。\n（已經寫入去評估報告！）')
    
    with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}過去五冬的平均盈餘配息率是{avg_cr:.2f}%。\n\n')
    if tk.messagebox.askquestion(title='訊息', message='敢欲繼續評估別个項目？')=='yes':
        getIS()
    else:
        root.destroy()
    return avg_cr

# 掠損益表
def getIS():
    global stk
    stk=entry.get()
    r = requests.get('https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=IS_M_QUAR&STOCK_ID='+str(stk),headers=headers)
    # RPT_CAT=IS_M_QUAR_ACC是逐季一直加甲年底(累季)，遮取單季，方便EPS划算

    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')
    iss=soup.find('table',id="tblFinDetail")
    
    file_path=os.path.join(directory_path, f"{stk}評估報告.txt")
    
    with open(file_path, 'a', encoding='utf-8') as f:
            f.write('三、利純情況佮預估殖利率(愛有趁錢，殖利率5%）\n')

    # 看毛利率佮營利率

    for tr in iss.find_all('tr'):
        if tr.find_all('td')!=[]:
            if '營業毛利'==tr.find('nobr').text.strip():
                gmr=tr.find_all('td')    # 毛利率佇這位的第3、5、7、9、11个td
                gmrs=[gmr[2].text.strip(),gmr[4].text.strip(),gmr[6].text.strip(),gmr[8].text.strip(),gmr[10].text.strip(),gmr[12].text.strip(),gmr[14].text.strip()]
                labelVar.set(f'{stk}最近這幾季的毛利率是：{gmrs}\n（已經寫入去評估報告！）')
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f'{stk}最近這幾季的毛利率是：{gmrs}!\n')
                neg_gm=[]
                for i in gmrs:
                    if float(i)<0:
                        neg_gm.append(i)
                if neg_gm==[]:
                    labelVar.set(f'{stk}毛利率攏正數，無問題！\n（已經寫入去評估報告！）')
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f'{stk}毛利率攏正數，無問題！\n')
                else:
                    labelVar.set(f'{stk}毛利率有負數，無閣考慮！\n（已經寫入去評估報告！')
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f'{stk}毛利率有負數，無閣考慮！\n')
                    continue
            
                        
            if '營業利益'==tr.find('nobr').text.strip():
                opr=tr.find_all('td')
                oprs=[opr[2].text.strip(),opr[4].text.strip(),opr[6].text.strip(),opr[8].text.strip(),opr[10].text.strip(),opr[12].text.strip(),opr[14].text.strip()]
                labelVar.set(f'{stk}最近這幾季的營利率是：{oprs}\n（已經寫入去評估報告！）')
                with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f'{stk}最近這幾季的營利率是：{oprs}\n')             
                neg_opr=[]
                for k in oprs:
                    if float(k)<0:
                        neg_opr.append(k)
                if neg_opr==[]:
                    labelVar.set(f'{stk}營利率攏正數，無問題！\n（已經寫入去評估報告！）')
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f'{stk}營利率攏正數，無問題！\n')
                else:
                    labelVar.set(f'{stk}營利率有負數，無閣考慮！\n（已經寫入去評估報告！）')
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f'{stk}營利率有負數，無閣考慮！\n')
                    continue
            
                
   # 粗估今年EPS
            if '每股稅後盈餘(元)'==tr.find('nobr').text.strip():
                epss=tr.find_all('td')
                eps=[epss[1].text.strip(),epss[3].text.strip(),epss[5].text.strip(),epss[7].text.strip(),epss[9].text.strip(),epss[11].text.strip(),epss[13].text.strip()]
                labelVar.set(f'{stk}最近這幾季的EPS是：{eps}\n（已經寫入去評估報告！）')
                with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f'{stk}最近這幾季的EPS是：{eps}\n')
                sum_eps=0
                for e in eps:
                    sum_eps+=float(e)
                avg_qeps=sum_eps/len(eps)
                pred_eps=avg_qeps*4
                if float(eps[0])<0 or float(eps[1])<0:
                    labelVar.set(f'{stk}利純變化傷大，無法度預測。\n（已經寫入去評估報告！）')
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f'{stk}利純變化傷大，無法度預測。\n')
                else:
                    labelVar.set(f'{stk}掠算今年的EPS是{pred_eps:.2f}。\n（已經寫入去評估報告！）')
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f'{stk}掠算今年的EPS是{pred_eps:.2f}。\n')

                        
    # 預估今年殖利率=估今年配息/股價

    # 掠即時股價

    stk_p = twstock.realtime.get(stk)['realtime']['latest_trade_price']

    pred_div_r=pred_eps/float(stk_p)
    if float(eps[0])<0 or float(eps[1])<0:
        labelVar.set(f'{stk}利純變化傷大，無法度預測{stk}今年的現金殖利率。\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}利純變化傷大，無法度預測{stk}今年的現金殖利率。\n')
    else:
        labelVar.set(f'划算今年{stk}現金殖利率是{pred_div_r*100:.2f}%。\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'划算今年{stk}現金殖利率是{pred_div_r*100:.2f}%。\n\n')
    if pred_div_r<0.05 or float(eps[0])<0 or float(eps[1])<0:
        labelVar.set(f'{stk}的預估現金殖利率傷低抑是真歹講，無閣考慮。\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}的預估現金殖利率傷低抑是真歹講，無閣考慮。\n\n')
    if tk.messagebox.askquestion(title='訊息', message='敢欲繼續評估別个項目？')=='yes':
        getBS()
    else:
        root.destroy()

# 掠資產負債表

def getBS():
    url = 'https://mops.twse.com.tw/mops/web/t164sb03'
    global stk
    stk=entry.get()
    form_data = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'keyword4': '',
        'code1': '',
        'TYPEK2': '',
        'checkbtn': '',
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'TYPEK': 'all',
        'isnew': 'true',
        'co_id': stk,
        'year': '',
        'season': ''
    }

    r = requests.post(url, params=form_data)
    soup = BeautifulSoup(r.text, 'html.parser')
    bss = soup.find('table', class_='hasBorder')
    
    file_path=os.path.join(directory_path, f"{stk}評估報告.txt")
    
    with open(file_path, 'a', encoding='utf-8') as f:
            f.write('四、資產構成情況(存貨一季袂使增加3成、兩季袂使增加5成；流動負債袂使超過30%閣較加流動資產）\n')

    trs = bss.find_all('tr')

    # 看存貨金額佔資產比趨勢

    inv_rates = []

    for tr in trs:
        if tr.find_all('td')!=[]:
            if '存貨' == tr.find_all('td')[0].text.strip():
                inv_rs=tr.find_all('td')
                inv_rates.append(inv_rs[2].text.strip())
                inv_rates.append(inv_rs[4].text.strip())
                inv_rates.append(inv_rs[6].text.strip())
    labelVar.set(f'{stk}過去這幾期的存貨佔資產比例是{inv_rates}(%)。\n（已經寫入去評估報告！）')
    with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}過去這幾期的存貨佔資產比例是{inv_rates}(%)。\n')
    
    if float(inv_rates[0])/float(inv_rates[1])>1.3 or float(inv_rates[0])/float(inv_rates[2])>1.5:
        labelVar.set(f'{stk}過去三冬存貨比例有變懸，無閣考慮！\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}過去三冬存貨比例有變懸，無閣考慮！\n')
    else:
        labelVar.set(f'{stk}的存貨比例看起來無問題！\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}的存貨比例看起來無問題！\n')

    
        
    # 流動負債率<30%

    liq_libs = []

    for tr in trs:
        if tr.find_all('td')!=[]:
            if '流動負債合計' == tr.find_all('td')[0].text.strip():
                liq_l=tr.find_all('td')
                liq_libs.append(liq_l[2].text.strip())
                liq_libs.append(liq_l[4].text.strip())
                liq_libs.append(liq_l[6].text.strip())
    labelVar.set(f'{stk}過去這幾期的流動負債比例是{liq_libs}(%)。\n（已經寫入去評估報告！）')
    with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}過去這幾期的流動負債比例是{liq_libs}(%)。\n')

    if float(liq_libs[0])/float(liq_libs[1])>1.3 and float(liq_libs[0])>float(liq_libs[2]):
        labelVar.set(f'{stk}過去一冬流動負債比例有變懸，無閣考慮！\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}過去一冬流動負債比例有變懸，無閣考慮！\n\n')

    elif float(liq_libs[0])/float(liq_libs[2])>1.5:
        labelVar.set(f'{stk}過去兩冬流動負債比例有變懸，無閣考慮！\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{stk}過去兩冬流動負債比例有變懸，無閣考慮！\n\n')
    elif float(liq_libs[0])>30:
        for tr in trs:
            if tr.find_all('td')!=[]:
                if '流動資產合計' == tr.find_all('td')[0].text.strip():
                    liq_ass=tr.find_all('td')[2].text.strip()
        if float(liq_ass)<float(liq_libs[0]):
            labelVar.set(f'{stk}流動負債比例超過30%，而且較懸流動資產，無閣考慮！\n（已經寫入去評估報告！）')
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'{stk}流動負債比例超過30%，而且較懸流動資產，無閣考慮！\n\n')
        else:
            labelVar.set(f'{stk}流動負債比例超過30%，毋過流動資產比例閣較懸。\n（已經寫入去評估報告！）')
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'{stk}流動負債比例超過30%，毋過流動資產比例閣較懸。\n\n')
    else:
        labelVar.set(f'{stk}流動負債比例看起來無問題！\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'{stk}流動負債比例看起來無問題！\n\n')
    if tk.messagebox.askquestion(title='訊息', message='敢欲繼續評估別个項目？')=='yes':
        getCF()
    else:
        root.destroy()

# 掠現金流量表
def getCF():
    global stk
    stk=entry.get()
    url = 'https://mops.twse.com.tw/mops/web/t164sb05'

    form_data = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'keyword4': '',
        'code1': '',
        'TYPEK2': '',
        'checkbtn': '',
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'TYPEK': 'all',
        'isnew': 'true',
        'co_id': stk,
        'year': '',
        'season': ''
    }

    r = requests.post(url, params=form_data)
    soup = BeautifulSoup(r.text, 'html.parser')
    bss = soup.find('table', class_='hasBorder')

    trs = bss.find_all('tr')
    
    file_path=os.path.join(directory_path, f"{stk}評估報告.txt")
    with open(file_path, 'a', encoding='utf-8') as f:
            f.write('五、現金收支情況(營業活動愛有現金流入)\n')

    
    # 營業現金流量愛是正數

    op_cfs = []

    for tr in trs:
        if tr.find_all('td')!=[]:
            if '營業活動之淨現金流入（流出）' == tr.find_all('td')[0].text.strip():
                opcfs=tr.find_all('td')
                op_cfs.append(opcfs[1].text.strip())
                op_cfs.append(opcfs[2].text.strip())

    labelVar.set(f'{stk}過去這兩年的營業活動純現金流量是{op_cfs}。\n（已經寫入去評估報告！）')
    with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'{stk}過去這兩年的營業活動純現金流量是{op_cfs}。\n')
    if float(op_cfs[0].replace(',',''))<0 or float(op_cfs[1].replace(',',''))<0:
        labelVar.set(f'{stk}過去兩冬捌有營業活動現金流出，無閣考慮！\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'{stk}過去兩冬捌有營業活動現金流出，無閣考慮！\n')
    else:
        labelVar.set(f'{stk}營業活動現金流量看起來無問題！\n（已經寫入去評估報告！）')
        with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'{stk}營業活動現金流量看起來無問題！\n')
    tk.messagebox.showinfo(title="訊息", message="評估結束，請參考評估報告！")


# GUI
root = tk.Tk()
root.geometry('280x300')
root.title("股票篩選器")

label_exp = tk.Label(root, text='請輸入股票代碼，了後選擇評估報告欲寄佇佗位。')
label_exp.grid(row=0, column=3, columnspan=5,pady=5,ipady=5)

entry = tk.Entry(root, justify='center')
entry.grid(row=1, column=5,pady=5,ipady=5,sticky='EW')

button = tk.Button(root, text="開始評估", command=rev_trend)
button.grid(row=2,column=5,pady=5,ipady=5)

labelVar = tk.StringVar()
labelVar.set('評估結果')

res_label = tk.Label(textvariable=labelVar,wraplength=270)
res_label.grid(row=3,column=3, columnspan=5,pady=5,ipady=5)

root.mainloop()
