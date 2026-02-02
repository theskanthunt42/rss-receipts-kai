import feedparser
import datetime
import time
import json
from urllib.parse import urlparse
import escpos.printer 

def setup():
    try:
        with open("config.json") as f:
            Data = f.read()
        try:
            _config = json.loads(Data)
        except json.JSONDecodeError as exp:
            print("Can't parse config.json for some reason, make sure it is in correct format.")
            print(exp)
            raise SystemExit
    except FileNotFoundError:
        print("Make sure you've got config.json in this folder.")
        raise SystemExit
    except PermissionError:
        print("Can't read config.json due to permission issues.")
    if "method" in _config and _config["method"] is not None or "":
        if _config["path"] is not None:
            if len(_config["feeds"]) > 0:
                pass
            else:
                print("Dude you gotta have at least one RSS source!")
                raise SystemExit
        else:
            print("Where's your printer mate?")
            raise SystemExit
    else:
        print("Config how you want to connect to your server, then come back.")
        raise SystemExit
        # Planned to do TCP/IP or Serial stuff, maybe later.
    return _config
    
    # validate URLs
    # Gotta skip validation of url for now         -the42game

def PrintRSS(conf):
    #UsbID = conf["path"]
    p = escpos.printer.Usb(idVendor=0x04b8, idProduct=0x0202)
    p.charcode()
    p.set(align="center")
    p.set(bold=True, double_height=True, double_width=True)
    p.textln("News Briefing")
    p.set(bold=False, double_height=False, double_width=False)
    p.textln(f"{datetime.datetime.now().strftime(format("%Y/%m/%d %H:%M:%S"))}")
    p.set(align="left")
    for srcs in conf["feeds"]:
        p.ln()
        try:
            d = feedparser.parse(srcs)
            p.set(bold=True)
            p.textln(d.feed.description)
            p.set(bold=False)
            p.textln(d.feed.link)
            p.ln()
            for entries in d.entries[:10]:
                p.set(bold=True)
                p.textln(entries.title)
                p.set(bold=False)
                p.textln(entries.description)
                p.ln(1)
                #print(f"{entries.title}\n{entries.description}")
        except Exception as e:
            print(e)
            pass
    p.ln(2)
    p.set(align="center")
    p.textln("END OF NEWS BRIEFING")
    p.cut()
    p.close()

def Job(conf):
    PrintRSS(conf)


def main():
    conf = setup()
    Job(conf)
        #time.sleep(21600)
    
    #for i in conf["schedule"]:
    #    schedule.every().day.at(f"{i}").do(Job(conf), "Time to print.")
    #while True:
    #    if input("Print now? [Y]"):
    #        Job(conf)
    #    schedule.run_pending()
        

if __name__ == '__main__':
    main()
