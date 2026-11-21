"""A deterministic, flat-colour illustrated newspaper front page."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

W=H=1024
NAVY="#102b42"; INK="#182f40"; PAPER="#f3ecd9"; WHITE="#fffaf0"
REG={"MIDDLE EAST":"#bd5a42","ASIA-PACIFIC":"#267d86","AMERICAS":"#4c6fa3","EUROPE":"#8871a0","AFRICA":"#b47b32","SCIENCE":"#497c68","WORLD":"#64717a"}
_cache={}
def F(path,size):
    key=(str(path),size)
    if key not in _cache: _cache[key]=ImageFont.truetype(str(path),size)
    return _cache[key]
def text(d,xy,s,f,c): d.text(xy,s,font=f,fill=c)
def ln(d,pts,c,w=2): d.line(pts,fill=c,width=w,joint="curve")
def wrap(d,s,f,width):
    out=[]; cur=""
    for word in s.split():
        t=word if not cur else cur+" "+word
        if cur and d.textlength(t,font=f)>width: out.append(cur);cur=word
        else:cur=t
    if cur:out.append(cur)
    return out
def burst(d,x,y,r,color):
    pts=[]
    for i in range(16):
        a=-math.pi/2+i*math.pi/8; rr=r if i%2==0 else r*.55
        pts.append((x+rr*math.cos(a),y+rr*math.sin(a)))
    d.polygon(pts,fill=color,outline="#fff0b8");d.ellipse((x-r*.25,y-r*.25,x+r*.25,y+r*.25),fill="#fff0b8")

def scene(name,regular,bold):
    im=Image.new("RGB",(320,104),"#e6dac1");d=ImageDraw.Draw(im)
    # Every panel gets a distinct, hand-drawn editorial scene in local coordinates.
    if name=="missile_calendar":
        d.rectangle((0,0,319,80),fill="#d87f59");d.rectangle((0,62,319,104),fill="#374752");d.ellipse((215,-22,292,56),fill="#f2c46b")
        for x,h in [(4,23),(25,31),(51,20),(74,36),(101,26),(125,31),(146,18)]:
            d.rectangle((x,77-h,x+18,80),fill="#273a46")
            for wx in range(x+4,x+16,7): d.rectangle((wx,80-h,wx+2,82-h),fill="#e1b976")
        d.polygon([(78,61),(143,61),(135,74),(86,74)],fill="#27323a");d.rectangle((103,25,119,63),fill="#27323a");d.polygon([(103,25),(111,8),(119,25)],fill="#ddd6c2");d.polygon([(103,45),(88,59),(103,55)],fill="#27323a");d.polygon([(119,45),(134,59),(119,55)],fill="#27323a")
        d.rectangle((207,54,294,101),fill="#fff4dc",outline=NAVY,width=2);d.rectangle((207,54,294,67),fill="#bd5144");text(d,(218,70),"2027",F(bold,22),NAVY);text(d,(221,91),"JAN 01",F(bold,8),"#68726c")
    elif name=="court":
        d.rectangle((0,0,320,104),fill="#e6dfca");d.rectangle((0,82,320,104),fill="#988d78")
        for x in (32,83,237,288): d.rectangle((x,25,x+22,87),fill="#f8f1df",outline="#9b927f",width=2);d.polygon([(x-5,26),(x+11,11),(x+27,26)],fill="#c8bda5")
        d.polygon([(202,33),(289,33),(276,43),(214,43)],fill="#a98c5e");ln(d,[(246,21),(246,68)],INK,5);d.ellipse((238,13,254,29),fill="#e9bd5e",outline=INK)
        ln(d,[(215,40),(206,68),(224,68),(215,40)],INK,3);ln(d,[(277,40),(268,68),(286,68),(277,40)],INK,3);ln(d,[(201,69),(229,69)],INK,4);ln(d,[(263,69),(291,69)],INK,4)
        d.polygon([(38,37),(57,18),(117,40),(105,59)],fill="#744c36",outline="#4e382b");d.polygon([(37,37),(50,23),(66,34),(53,48)],fill="#82563a",outline="#4e382b");ln(d,[(106,48),(170,78)],"#d3aa6a",9);ln(d,[(99,44),(164,75)],"#654833",2)
        d.polygon([(171,78),(197,80),(204,85),(178,85)],fill="#744c36");text(d,(240,89),"9 : 6",F(bold,11),"#536d68")
    elif name=="ipo":
        d.rectangle((0,0,320,104),fill="#c9e0db");d.rectangle((0,72,320,104),fill="#637b80")
        for x,h in [(4,24),(27,38),(54,27),(80,48),(111,31),(137,41),(164,25),(190,45),(221,32),(248,51),(279,38),(301,27)]:
            d.rectangle((x,72-h,x+19,72),fill="#405b65")
            for wx in range(x+4,x+17,7):d.rectangle((wx,76-h,wx+2,77-h),fill="#f4d17d")
        d.rounded_rectangle((88,51,220,98),radius=7,fill="#183d56",outline="#0c283b",width=3)
        for x in range(100,211,12):d.rectangle((x,46,x+5,53),fill="#f2bd4d");d.rectangle((x,96,x+5,103),fill="#f2bd4d")
        text(d,(125,68),"AI",F(bold,22),"#e5f0e7")
        for x,h in [(239,24),(256,36),(273,50)]:d.rectangle((x,72-h,x+12,72),fill="#3a9b70")
        ln(d,[(235,48),(263,27),(281,17)],"#197a55",6);d.polygon([(274,16),(294,12),(285,30)],fill="#197a55");text(d,(241,80),"+17%",F(bold,12),"#155b45")
    elif name=="kyiv":
        d.rectangle((0,0,320,104),fill="#263a58");d.rectangle((0,81,320,104),fill="#27323a");ln(d,[(8,85),(92,20),(111,85)],"#7789a0",5);ln(d,[(222,84),(305,11),(311,84)],"#7789a0",5)
        for x,h in [(5,33),(29,45),(62,29),(91,53),(119,40),(214,29),(241,47),(274,37),(298,52)]:
            d.rectangle((x,81-h,x+20,81),fill="#435168")
            for wx in (x+4,x+12):d.rectangle((wx,84-h,wx+3,87-h),fill="#e7bd69")
        # Smoke rises behind two hot, high-contrast impact bursts.
        for cx,cy in ((54,25),(260,23)):
            d.ellipse((cx-17,cy-7,cx+2,cy+12),fill="#717681");d.ellipse((cx-7,cy-15,cx+12,cy+8),fill="#8b8b8a");d.ellipse((cx+2,cy-10,cx+20,cy+9),fill="#626b78")
        # Leaning, fractured apartment block with broken roofline and exposed windows.
        d.polygon([(142,43),(184,34),(196,96),(151,101)],fill="#8a786d",outline="#e2b18b");d.polygon([(142,43),(153,33),(161,40),(169,28),(179,36),(188,31),(184,34)],fill="#9a7967")
        for y in (49,64,79,91):
            for x in (149,164,178):d.polygon([(x,y),(x+7,y-1),(x+8,y+7),(x+1,y+8)],fill="#28384a")
        ln(d,[(161,48),(174,60),(165,72),(182,85)],"#f0a06d",3);ln(d,[(173,58),(187,54)],"#f2c47e",2)
        burst(d,52,28,24,"#ff9a32");burst(d,52,28,14,"#ffd34f");burst(d,260,26,23,"#ff9a32");burst(d,260,26,13,"#ffd34f")
        ln(d,[(55,40),(26,91)],"#f3d18b",3);ln(d,[(254,39),(284,88)],"#f3d18b",3)
    elif name=="tanker":
        d.rectangle((0,0,320,104),fill="#afd0ce");d.polygon([(0,0),(75,0),(99,55),(85,76),(0,78)],fill="#68766a");d.polygon([(320,0),(254,0),(232,52),(245,78),(320,79)],fill="#74806c")
        for y in (77,88,99):ln(d,[(0,y),(55,y-3),(110,y+2),(165,y-2),(220,y+2),(275,y-3),(320,y)],"#317d8a",3)
        d.polygon([(85,61),(237,61),(217,84),(105,84),(89,74)],fill="#263b4b");d.rectangle((131,43,198,62),fill="#d9d7c7",outline="#18374a",width=2);d.rectangle((199,50,216,63),fill="#f1eee0",outline="#18374a",width=2)
        for x in range(139,195,13):d.rectangle((x,47,x+7,52),fill="#65808a")
        d.rectangle((104,72,217,78),fill="#bd5847");burst(d,221,40,10,"#ef9a46");d.ellipse((216,18,232,37),fill="#85867d");d.ellipse((226,11,244,29),fill="#92928a");text(d,(14,87),"HORMUZ",F(bold,9),"#f8f0d8")
    elif name=="ballot":
        d.rectangle((0,0,320,104),fill="#d4e0d9");d.rectangle((0,77,320,104),fill="#a29a85");d.rectangle((95,31,225,81),fill="#e6ddc7",outline="#7f8178",width=2);d.polygon([(85,33),(160,8),(235,33)],fill="#b9a87c",outline="#736d5f");d.ellipse((138,17,182,53),fill="#d4c49d",outline="#736d5f",width=2);d.rectangle((152,29,168,81),fill="#d8c9a8")
        for x in (111,143,175,207):d.rectangle((x,48,x+7,73),fill="#a99d81");d.polygon([(x-4,49),(x+3,43),(x+11,49)],fill="#a99d81")
        d.rounded_rectangle((226,67,298,101),radius=4,fill="#315b68",outline="#1b3945",width=3);d.rectangle((235,72,289,79),fill="#192f3b");d.polygon([(191,47),(238,53),(234,72),(187,66)],fill="#fff8e9",outline="#6e7068",width=2);d.rectangle((201,54,222,57),fill="#be5948");ln(d,[(189,44),(212,25),(235,22)],"#c79254",8);d.ellipse((181,37,199,53),fill="#d9a976")
    elif name=="cyclone":
        d.rectangle((0,0,320,104),fill="#c4d8d4");d.polygon([(0,70),(69,61),(120,72),(171,66),(224,77),(320,70),(320,104),(0,104)],fill="#3b93a1");d.polygon([(216,0),(320,0),(320,104),(266,104),(253,86),(240,67),(250,49),(232,33)],fill="#d9c69c")
        for cx,cy in ((274,60),(298,84)):
            ln(d,[(cx,cy),(cx-7,cy-26)],"#5d553f",3);ln(d,[(cx-7,cy-24),(cx-25,cy-33)],"#5d553f",2);ln(d,[(cx-7,cy-24),(cx+9,cy-38)],"#5d553f",2)
        for r in (38,28,18,8):d.arc((41-r,42-r,41+r,42+r),20,330,fill="#6284a0",width=5)
        d.ellipse((35,36,47,48),fill="#5b7892")
        # A curved shoreline anchors the tiny evacuees; arrow points inland.
        ln(d,[(10,97),(48,92),(88,94),(126,89),(166,92),(206,85)],"#e8d5ad",4)
        ln(d,[(108,99),(182,76)],"#ab563f",4);d.polygon([(180,70),(194,72),(185,83)],fill="#ab563f")
        for x in (113,132,151,170):
            d.ellipse((x,76,x+7,83),fill="#344957");ln(d,[(x+4,83),(x+4,95)],"#344957",3);ln(d,[(x+4,87),(x-1,92)],"#344957",2);d.rectangle((x+6,85,x+12,93),fill="#b77a43")
        text(d,(18,87),"ODISHA",F(bold,8),"#eff0df")
    elif name=="stocks":
        d.rectangle((0,0,320,104),fill="#e7e1d1");d.rectangle((0,83,320,104),fill="#c4baa4")
        for y in (22,43,64,82):ln(d,[(15,y),(305,y)],"#c8c4b7",1)
        for x in (38,76,114,152,190,228,266):ln(d,[(x,14),(x,84)],"#d1ccbe",1)
        pts=[(18,24),(58,27),(89,20),(124,35),(158,33),(194,53),(229,47),(261,71),(300,86)];ln(d,pts,"#be4c48",5)
        for x,y in pts:d.ellipse((x-3,y-3,x+3,y+3),fill="#be4c48")
        d.polygon([(155,7),(187,7),(201,21),(201,49),(187,63),(155,63),(141,49),(141,21)],fill="#c44138",outline="#fff3df");text(d,(154,25),"STOP",F(bold,13),"white");d.rectangle((171,63,186,94),fill="#d7aa82");d.rounded_rectangle((162,79,194,99),radius=12,fill="#dfb58f")
        for x in (163,172,181,190):d.ellipse((x,71,x+8,86),fill="#e2b993")
        text(d,(14,91),"3-DAY FALL",F(bold,8),"#5d5450")
    elif name=="airport":
        d.rectangle((0,0,320,104),fill="#20334b");d.rectangle((0,80,320,104),fill="#313c47");ln(d,[(0,94),(320,94)],"#b7ab8b",2)
        for x in (12,47,82,117,152,187,222,257,292):d.rectangle((x,92,x+13,95),fill="#e8dcad")
        d.rectangle((264,24,286,80),fill="#687b86");d.rectangle((253,20,298,31),fill="#82919a");d.rectangle((268,14,282,20),fill="#82919a");ln(d,[(275,17),(275,6)],"#e9c16a",2)
        d.ellipse((117,68,207,82),fill="#c5d1d1");d.polygon([(204,71),(231,65),(211,77)],fill="#c5d1d1");d.polygon([(148,69),(167,55),(174,55),(169,69)],fill="#b5c5c8");d.polygon([(148,78),(165,92),(173,92),(169,78)],fill="#aebdc1")
        # Large foreground quadcopter: four arms and rotor discs read at thumbnail size.
        drone="#101b2b";edge="#9caab1"
        for a,b in ((111,13),(218,13),(111,54),(218,54)):
            d.ellipse((a-17,b-7,a+17,b+7),fill=drone,outline="#d0d7d2",width=2)
            ln(d,[(a-11,b),(a+11,b)],"#71818c",1)
        for pt in ((120,20),(208,20),(120,48),(208,48)):
            ln(d,[(159,31),pt],drone,7);ln(d,[(159,31),pt],edge,1)
        d.polygon([(147,25),(158,21),(171,25),(175,34),(166,40),(153,39),(145,33)],fill=drone,outline="#c1c9c8")
        d.ellipse((155,27,163,35),fill="#e3bd70");d.polygon([(153,38),(166,38),(170,47),(160,51)],fill=drone)
    elif name=="talks":
        d.rectangle((0,0,320,104),fill="#d8dfd4");d.rectangle((0,77,320,104),fill="#a69a7d");d.polygon([(21,47),(80,17),(139,47)],fill="#777e70");d.rectangle((32,46,128,84),fill="#d5c7a4",outline="#787568",width=2)
        for x in (45,70,95,115):d.rectangle((x,52,x+8,83),fill="#ad9c79")
        ln(d,[(183,12),(183,51)],"#4d5c5c",2);d.rectangle((185,14,218,30),fill="#f3f0df");d.rectangle((185,20,218,25),fill="#344c81");ln(d,[(229,12),(229,51)],"#4d5c5c",2);d.rectangle((231,14,264,30),fill="#efeadd");d.rectangle((231,14,243,30),fill="#dc5145");d.rectangle((252,14,264,30),fill="#5076ae")
        d.polygon([(40,83),(268,83),(307,102),(10,102)],fill="#6c5845");d.polygon([(105,82),(211,82),(226,96),(95,96)],fill="#e0d3b4",outline="#9c9078");ln(d,[(129,84),(146,90),(166,84),(188,92)],"#899c90",2)
        # Two suit-clad forearms meet in a broad, central clasp.
        d.polygon([(0,48),(93,50),(137,58),(152,70),(137,83),(91,76),(0,78)],fill="#263e54")
        d.polygon([(320,48),(227,50),(183,58),(168,70),(183,83),(229,76),(320,78)],fill="#34495b")
        d.polygon([(124,55),(145,59),(153,68),(143,76),(127,71)],fill="#f2e9d9");d.polygon([(196,55),(175,59),(167,68),(177,76),(193,71)],fill="#f2e9d9")
        d.polygon([(141,59),(159,58),(174,64),(192,64),(198,71),(188,78),(174,75),(160,72),(147,77),(137,70)],fill="#d9a782",outline="#a36e54")
        d.polygon([(174,62),(187,59),(199,64),(193,69),(182,68)],fill="#e4b48b",outline="#a36e54");ln(d,[(163,69),(178,72),(188,71)],"#a36e54",2)
    elif name=="aid":
        d.rectangle((0,0,320,104),fill="#b9c9c7");d.rectangle((0,74,320,104),fill="#4d91a0")
        for x,y in ((34,19),(99,26),(164,16),(245,22),(286,4)):ln(d,[(x,y),(x-8,y+17)],"#637c86",2);ln(d,[(x+12,y+3),(x+2,y+22)],"#637c86",2)
        for x in (20,100,220):d.polygon([(x,55),(x+25,35),(x+50,55)],fill="#d4c1a0",outline="#857b69");d.polygon([(x+8,53),(x+42,53),(x+38,76),(x+12,76)],fill="#bba987")
        d.rectangle((56,65,154,87),fill="#d1d1c1",outline="#667a7d",width=2);d.rectangle((67,56,123,68),fill="#d1d1c1",outline="#667a7d",width=2);d.rectangle((62,74,95,86),fill="#c29451");d.rectangle((101,74,134,86),fill="#c29451");text(d,(67,74),"AID",F(bold,8),"#493e32")
        d.ellipse((71,84,90,103),fill="#283943");d.ellipse((130,84,149,103),fill="#283943")
        for x in (183,197,211,226,242):d.ellipse((x,69,x+7,76),fill="#34464e");ln(d,[(x+4,76),(x+4,93)],"#34464e",3)
        text(d,(17,91),"FLOODWATER",F(bold,8),"#f4edda")
    else: # giant-star science image
        d.rectangle((0,0,320,104),fill="#182742")
        for x,y,r in ((19,19,2),(46,62,2),(82,18,2),(122,27,1),(193,16,2),(234,50,2),(283,17,2),(301,71,2),(36,94,1),(269,94,1),(111,78,1)):d.ellipse((x-r,y-r,x+r,y+r),fill="#e9e1cb")
        # A luminous spiral stream runs from the companion toward the giant star.
        for i in range(62):
            t=i/61;angle=math.pi*2.15*t;radius=158-111*t
            x=96+radius*math.cos(angle);y=49+radius*.34*math.sin(angle)
            r=1.5+2.1*t
            c="#f5c75f" if i%4 else "#fff0a6"
            d.ellipse((x-r,y-r,x+r,y+r),fill=c)
        # Concentric flat-colour glow discs, rays, core and bright companion.
        for box,c in (((24,-13,168,111),"#4a426f"),((36,-2,158,99),"#85639a"),((49,9,145,89),"#c2776c"),((58,18,135,80),"#f1ad57")):
            d.ellipse(box,fill=c)
        for a in range(0,360,30):
            ar=math.radians(a);r1=42;r2=60
            ln(d,[(96+r1*math.cos(ar),49+r1*.74*math.sin(ar)),(96+r2*math.cos(ar),49+r2*.74*math.sin(ar))],"#ffd976",3)
        d.ellipse((68,21,124,77),fill="#ffe58b",outline="#fff4c7",width=3);d.ellipse((78,30,115,68),fill="#fff7d7")
        d.ellipse((238,45,272,79),fill="#d16f5e",outline="#ffd783",width=3);d.ellipse((246,51,264,69),fill="#ffe4a0")
        d.polygon([(268,85),(306,65),(313,73),(277,93)],fill="#111e30");d.polygon([(265,81),(275,77),(281,88),(271,93)],fill="#263952");ln(d,[(284,88),(279,104)],"#111e30",4);ln(d,[(302,77),(309,104)],"#111e30",4)
    return im

def draw_map(im,leads,bf,bold_path):
    d=ImageDraw.Draw(im);d.rectangle((0,110,W,206),fill="#b8d1cb")
    land="#819b8d";edge="#6e897e"
    continents=[
      # North America, including Alaska and the Gulf-facing coast.
      [(65,136),(75,130),(91,128),(104,123),(120,126),(133,124),(148,130),(160,136),(171,142),(166,149),(155,151),(150,157),(138,159),(131,166),(122,163),(116,155),(105,153),(95,150),(84,147),(73,143)],
      # Central America and the tapering South American landmass.
      [(142,156),(152,157),(160,162),(165,168),(171,171),(166,175),(159,171),(154,166)],
      [(153,168),(165,166),(176,172),(184,182),(185,191),(178,202),(171,198),(166,187),(161,178)],
      # Greenland.
      [(229,132),(237,125),(252,125),(264,130),(273,139),(267,145),(253,144),(246,139),(237,140)],
      # Europe and Asia form one recognizable mainland with a stepped southern coast.
      [(400,139),(411,132),(420,126),(435,126),(448,131),(460,128),(472,135),(483,131),(495,136),(507,134),(518,138),(530,135),(541,139),(555,135),(570,140),(584,139),(598,143),(613,140),(629,144),(646,141),(661,146),(678,143),(695,148),(712,145),(729,151),(746,149),(761,154),(779,151),(797,156),(813,153),(833,158),(850,156),(869,162),(888,160),(900,166),(893,171),(881,175),(869,172),(855,179),(840,175),(829,181),(815,177),(803,183),(792,179),(781,183),(773,176),(766,185),(760,191),(754,183),(751,175),(743,171),(734,172),(727,179),(724,188),(720,196),(714,185),(711,174),(705,169),(697,168),(688,169),(678,163),(667,166),(656,160),(644,163),(632,157),(620,162),(609,156),(597,161),(585,157),(573,161),(561,155),(551,159),(539,152),(527,157),(514,150),(503,153),(493,148),(481,151),(472,147),(460,150),(449,146),(438,148),(427,143),(416,146),(406,143)],
      # Africa is distinct below the visible Mediterranean water gap.
      [(451,160),(462,157),(476,158),(488,161),(500,159),(510,164),(508,174),(503,183),(500,192),(491,202),(484,197),(480,188),(474,180),(466,173),(458,169)],
      # Japan and the island chains of maritime Southeast Asia.
      [(843,170),(849,173),(850,180),(846,184),(842,178)],
      [(781,184),(790,185),(794,190),(789,193),(783,189)],
      [(803,185),(811,186),(816,190),(812,193),(806,190)],
      # Australia remains at the same place in the band.
      [(902,179),(927,177),(943,183),(939,192),(922,194),(910,188)]]
    for p in continents:d.polygon(p,fill=land,outline=edge)
    d.ellipse((289,128,324,143),fill=land,outline=edge)
    # Approximate locations; close pins are gently offset to remain individually legible.
    pins={1:(654,150),2:(826,159),3:(157,157),4:(568,155),5:(684,173),6:(620,161),7:(769,174),8:(852,154),9:(516,163),10:(542,137),11:(595,183)}
    for item in leads:
        n=item["id"]
        if n not in pins:continue
        x,y=pins[n];c=REG[item["region"]];d.ellipse((x-10,y-10,x+10,y+10),fill=c,outline="#fff5df",width=2)
        f=bf; bb=d.textbbox((0,0),str(n),font=f);text(d,(x-(bb[2]-bb[0])/2,y-(bb[3]-bb[1])/2-1),str(n),f,"white")
    star=[]
    for k in range(10):
        a=-math.pi/2+k*math.pi/5;rr=15 if k%2==0 else 7
        star.append((966+rr*math.cos(a),124+rr*math.sin(a)))
    d.polygon(star,fill="#f5d77d",outline="#9f7841");text(d,(960,120),"12",F(bold_path,8),NAVY)
    text(d,(858,140),"ANDROMEDA",FONTS["map"],NAVY);text(d,(18,114),"WORLD / LEAD DATELINES",FONTS["map"],NAVY)

FONTS={}
def draw_leads(im,leads,regular,bold):
    d=ImageDraw.Draw(im); x0,y0=17,210;cw,ch=241,149;gx,gy=6,4
    for i,item in enumerate(leads):
        col,row=i%4,i//4;x=x0+col*(cw+gx);y=y0+row*(ch+gy);accent=REG[item["region"]]
        d.rounded_rectangle((x,y,x+cw,y+ch),radius=5,fill=WHITE,outline="#c9c0ad",width=1);d.rectangle((x,y+5,x+4,y+ch-5),fill=accent)
        art=scene(item["scene"],regular,bold).resize((cw-12,76),Image.Resampling.LANCZOS);im.paste(art,(x+7,y+5))
        hf=F(bold,13);hl=wrap(d,item["headline"],hf,cw-14)
        while len(hl)>2 and hf.size>9:hf=F(bold,hf.size-1);hl=wrap(d,item["headline"],hf,cw-14)
        hy=y+84
        for j,s in enumerate(hl):text(d,(x+8,hy+j*(hf.size+1)),s,hf,INK)
        df=F(regular,8);dl=wrap(d,item["detail"],df,cw-15)
        while len(dl)>2 and df.size>7:df=F(regular,df.size-1);dl=wrap(d,item["detail"],df,cw-15)
        dy=hy+max(hf.size+1,len(hl)*(hf.size+1))+1
        for j,s in enumerate(dl):text(d,(x+8,dy+j*(df.size+1)),s,df,"#48575a")
        ty=y+ch-15;d.rounded_rectangle((x+8,ty,x+cw-8,ty+11),radius=3,fill="#efe7d4");text(d,(x+12,ty+1),f'{item["id"]:02d}  {item["region"]} / {item["section"]}',F(bold,7),accent)

def draw_numbers(im,nums):
    d=ImageDraw.Draw(im);y=669;h=65;d.rectangle((0,y,W,y+h),fill="#e4dbc7");text(d,(17,y+5),"THE DAY IN NUMBERS",FONTS["section"],NAVY)
    cell=136;start=196
    for i,n in enumerate(nums):
        x=start+i*cell
        if i:d.line((x-8,y+22,x-8,y+h-5),fill="#b8af9d",width=1)
        text(d,(x,y+23),n["value"],FONTS["num"],INK);bx=x;by=y+44;bw=104;bh=10
        d.rounded_rectangle((bx,by,bx+bw,by+bh),radius=4,fill="#c5bcaa")
        if "split" in n:
            one=int(bw*n["split"][0]/sum(n["split"]));d.rounded_rectangle((bx,by,bx+one,by+bh),radius=4,fill="#477d6a");d.rectangle((bx+one-1,by,bx+bw,by+bh),fill="#c45a49")
        else:d.rounded_rectangle((bx,by,bx+bw*n["amount"],by+bh),radius=4,fill="#438270")
        text(d,(x,y+56),n["caption"],FONTS["numcap"],"#465755")

def draw_briefs(im,briefs):
    d=ImageDraw.Draw(im);y0=738;bottom=978;d.rectangle((0,y0,W,bottom),fill="#f7f1e2");text(d,(17,y0+4),"THE REST OF THE WORLD",FONTS["section"],NAVY);text(d,(798,y0+5),"38 BRIEFS  /  EVERY REGION",FONTS["smallhead"],"#5f706e")
    start=y0+24;gap=12;cw=241;groups=[briefs[k::4] for k in range(4)]
    for col,group in enumerate(groups):
        x=17+col*(cw+gap);y=start;end=17+(col+1)*(cw+gap)-gap
        for b in group:
            label=b["region"];lf=FONTS["region"];lw=d.textlength(label,font=lf);text(d,(x,y),label,lf,REG[label]);tx=x+lw+5;lines=wrap(d,b["text"],FONTS["brief"],end-tx)
            for s in lines:text(d,(tx,y),s,FONTS["brief"],"#34444a");y+=9
            y+=2

def draw_footer(im,data):
    d=ImageDraw.Draw(im);d.rectangle((12,982,1012,1020),fill="#efe5d1",outline="#9f9a88",width=1)
    lines=wrap(d,data["date_check"],FONTS["date"],980)
    for i,s in enumerate(lines[:2]):text(d,(20,984+i*8),s,FONTS["date"],"#695b4b")
    d.line((20,1002,1004,1002),fill="#c3b8a1",width=1);w=d.textlength(data["closing"],font=FONTS["closing"]);text(d,((W-w)/2,1005),data["closing"],FONTS["closing"],NAVY)

def render(data,output_path,assets_dir):
    regular=assets_dir/"DejaVuSans.ttf";bold=assets_dir/"DejaVuSans-Bold.ttf"
    FONTS.update({"map":F(bold,9),"section":F(bold,12),"num":F(bold,15),"numcap":F(regular,7),"smallhead":F(bold,9),"region":F(bold,6),"brief":F(regular,7),"date":F(regular,7),"closing":F(bold,10)})
    im=Image.new("RGB",(W,H),PAPER);d=ImageDraw.Draw(im);d.rectangle((0,0,W,110),fill=NAVY);d.rectangle((0,0,12,110),fill="#c95943")
    text(d,(27,8),"THE WORLD IN ONE IMAGE",F(bold,22),"#f4e9cf");d.line((27,37,996,37),fill="#657584",width=1)
    text(d,(25,41),data["date"],F(bold,34),"#fff4db");text(d,(28,82),data["subhead"],F(bold,12),"#e2b966");text(d,(592,84),data["sources"],F(regular,10),"#e6e4d8")
    draw_map(im,data["leads"],F(bold,10),bold);draw_leads(im,data["leads"],regular,bold);draw_numbers(im,data["numbers"]);draw_briefs(im,data["briefs"]);draw_footer(im,data)
    im.save(output_path,format="PNG",optimize=True,compress_level=9)
