# lsrc='forloops'
# lres='fxrlxxps'
lsrc='forloops'
lres='fxrlxxp'
# lsrc='forloops'
# lres='frlpz'
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
    for res_idx, each_res in enumerate(lres):
        # print(idx, each_res)
        src_idx=lsrc.find(each_res)
        # print(j)
        if src_idx-res_idx==1:
            quite=lsrc[src_idx-1]
            print(((src-res-set(quite)).pop())+' '+((res-src).pop()))  
            print(quite)
            break
    if quite is None:
        quite=lsrc[-1]
        print(((src-res-set(quite)).pop())+' '+((res-src).pop()))  
        print(quite)
