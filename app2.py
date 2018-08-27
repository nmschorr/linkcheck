from src.linkcheck import linkcheck

class app2(object):
    from pathlib import Path
    filenme = Path("./src/runargs.txt")
    res, res_list = 1, []
    with open(filenme, 'r+') as file:
        while res:
            res = file.readline()
            if not res.startswith('#'):
                res_list.append(res.rstrip())
    if res_list:
        res_list.pop(-1)  # last one comes in empty
    for site in res_list:
        lc = linkcheck()
        answer = lc.main_run(site)
        #print('printing from app2')
        for a in answer:
            print(a)
app2()