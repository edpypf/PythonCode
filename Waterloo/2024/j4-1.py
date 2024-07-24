# lsrc='forloops'
# lres='fxrlxxps'
# lsrc='forloops'
# lres='fxrlxxp'
lsrc='forloops'
lres='frlpz'
# lsrc=input()
# lres=input()

src=set(lsrc)
res=set(lres)
quite=None
if len(lsrc)==len(lres):
    quite='-'
    # display sily key and wrong letter
    print(((src-res).pop())+' '+((res-src).pop()))  
    print(quite)
else:
    for src_idx, each_src in enumerate(lsrc):
        res_idx=lres.find(each_src)
        if src_idx!=len(lres):
            if res_idx==-1:
                exists=lsrc.find(lres[src_idx])
                if exists!=-1:
                    quite=lsrc[src_idx]
                    print(((src-res-set(quite)).pop())+' '+((res-src).pop()))  
                    print(quite)
                    break 
        else:
            quite=lsrc[src_idx]
            print(((src-res-set(quite)).pop())+' '+((res-src).pop()))  
            print(quite)
            break