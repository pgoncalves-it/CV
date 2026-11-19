from PIL import Image, ImageDraw, ImageFont
import sys, json, urllib.request
URL="https://cv-patrick-default-rtdb.europe-west1.firebasedatabase.app/avis.json"
def stats():
    d=json.load(urllib.request.urlopen(URL,timeout=20)) or {}
    L=d.values() if isinstance(d,dict) else d
    L=[v for v in L if v and len(v.get("notes",[]))==4]
    return (sum(sum(v["notes"])/4 for v in L)/len(L),len(L)) if L else (0.0,0)
if len(sys.argv)>2: avg,n=float(sys.argv[1]),int(sys.argv[2])
else:
    try: avg,n=stats()
    except Exception as e: sys.exit("Lecture impossible : "+str(e))
W,H=1200,627
img=Image.new("RGB",(W,H))
d=ImageDraw.Draw(img)
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=(int(14+10*t),int(30+30*t),int(54+50*t)))
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s:ImageFont.truetype(p,s)
gold=(245,184,74); grey=(70,88,115); white=(255,255,255); soft=(190,205,225); blue=(90,169,240)
d.rectangle([60,70,70,560],fill=gold)
d.text((100,70),"MON CV EN LIGNE",font=f(B,28),fill=blue)
d.text((100,120),"Patrick Gonçalves",font=f(B,66),fill=white)
d.text((100,198),"Cardoso",font=f(B,66),fill=white)
d.text((100,285),"Technicien IT confirmé",font=f(R,36),fill=soft)
# stars: grey base + gold clipped by average
sf=f(B,70); x0,y0=100,350
txt="★★★★★★"
d.text((x0,y0),txt,font=sf,fill=grey)
l,t,r,b=d.textbbox((x0,y0),txt,font=sf)
frac=max(0,min(1,avg/6))
if frac>0:
    layer=Image.new("RGBA",(W,H),(0,0,0,0)); ld=ImageDraw.Draw(layer)
    ld.text((x0,y0),txt,font=sf,fill=gold+(255,))
    mask=Image.new("L",(W,H),0); ImageDraw.Draw(mask).rectangle([l,t,l+(r-l)*frac,b],fill=255)
    img.paste(layer,(0,0),Image.composite(layer.split()[3],Image.new("L",(W,H),0),mask))
    d=ImageDraw.Draw(img)
if n>0:
    lab=f"{avg:.1f}".replace(".",",")+" / 6  ·  "+str(n)+(" votants" if n>1 else " votant")
else:
    lab="Pas encore d’avis : soyez le premier à noter"
d.text((x0+r-l+25,y0+22),"" ,font=f(R,30),fill=soft)
d.text((100,440),lab,font=f(B,32) if n>0 else f(R,32),fill=white)
d.rounded_rectangle([100,500,820,566],radius=33,fill=blue)
d.text((135,515),"pgoncalves-it.github.io/CV",font=f(B,34),fill=(10,25,45))
cx,cy,r=990,170,105
d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=gold,width=7)
if n>0:
    d.text((cx,cy-12),f"{avg:.1f}".replace(".",","),font=f(B,84),fill=gold,anchor="mm")
    d.text((cx,cy+58),"sur 6",font=f(R,28),fill=white,anchor="mm")
else:
    d.text((cx,cy),"★",font=f(B,130),fill=gold,anchor="mm")
import qrcode
q=qrcode.QRCode(border=1,box_size=7,error_correction=qrcode.constants.ERROR_CORRECT_M)
q.add_data("https://pgoncalves-it.github.io/CV/");q.make(fit=True)
qi=q.make_image(fill_color="black",back_color="white").convert("RGB")
qw=qi.size[0]
d.rounded_rectangle([cx-qw//2-10,305,cx+qw//2+10,305+qw+20],radius=14,fill="white")
img.paste(qi,(cx-qw//2,315))
d.text((cx,305+qw+48),"Scannez pour voir mon CV",font=f(B,22),fill=white,anchor="mm")
img.save("image-linkedin-cv.png")
