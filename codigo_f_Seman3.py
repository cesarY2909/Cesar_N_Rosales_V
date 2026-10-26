import random, math, time, json, statistics as st
import matplotlib.pyplot as plt
N=20
random.seed(42)
CIU=[(random.random()*100,random.random()*100) for _ in range(N)]
def costo(r): return sum(math.dist(CIU[r[i]],CIU[r[(i+1)%N]]) for i in range(N))
def vecino(r):
    i,j=sorted(random.sample(range(N),2)); return r[:i]+r[i:j+1][::-1]+r[j+1:]  # 2-opt
def hill_climbing(iters=20000):
    act=random.sample(range(N),N); c=costo(act); h=[c]
    for _ in range(iters):
        v=vecino(act); cv=costo(v)
        if cv<c: act,c=v,cv
        h.append(c)
    return act,c,h
def sa(T0=100.0,Tmin=1e-3,alpha=0.9995,iters=20000):
    act=random.sample(range(N),N); c=costo(act); mejor,cm=act[:],c; T=T0; h=[cm]
    for _ in range(iters):
        v=vecino(act); cv=costo(v); d=cv-c
        if d<0 or random.random()<math.exp(-d/T): act,c=v,cv
        if c<cm: mejor,cm=act[:],c
        T=max(T*alpha,Tmin); h.append(cm)
    return mejor,cm,h
R={"HC":[], "SA":[]}; tm={"HC":[], "SA":[]}; H1=H2=None; B1=B2=None
for k in range(10):
    random.seed(100+k)
    t=time.perf_counter(); r,c,h=hill_climbing(); tm["HC"].append(time.perf_counter()-t); R["HC"].append(c)
    if k==0: H1=h; B1=r
    random.seed(100+k)
    t=time.perf_counter(); r,c,h=sa(); tm["SA"].append(time.perf_counter()-t); R["SA"].append(c)
    if k==0: H2=h; B2=r
out={}
for a in R: out[a]={"mejor":round(min(R[a]),2),"media":round(st.mean(R[a]),2),"desv":round(st.pstdev(R[a]),2),"peor":round(max(R[a]),2),"tiempo_s":round(st.mean(tm[a]),2)}
out["params"]={"N":N,"iters":20000,"T0":100.0,"Tmin":1e-3,"alpha":0.9995}
plt.figure(figsize=(7,4)); plt.plot(H1,label="Hill Climbing"); plt.plot(H2,label="Simulated Annealing")
plt.xlabel("Iteración"); plt.ylabel("Mejor costo (distancia)"); plt.title("Convergencia (ejecución 1)"); plt.legend(); plt.grid(alpha=.3)
plt.savefig("fig/s3_conv.png",dpi=160,bbox_inches="tight"); plt.close()
fig,ax=plt.subplots(1,2,figsize=(10,4.2))
for a,r,t in ((ax[0],B1,"Hill Climbing"),(ax[1],B2,"Simulated Annealing")):
    xs=[CIU[i][0] for i in r+[r[0]]]; ys=[CIU[i][1] for i in r+[r[0]]]
    a.plot(xs,ys,"-o",ms=4); a.set_title(f"{t}: {costo(r):.1f}")
plt.savefig("fig/s3_rutas.png",dpi=160,bbox_inches="tight"); plt.close()
plt.figure(figsize=(6,4)); plt.boxplot([R["HC"],R["SA"]],labels=["Hill Climbing","Sim. Annealing"]); plt.ylabel("Costo final (10 ejecuciones)")
plt.savefig("fig/s3_box.png",dpi=160,bbox_inches="tight"); plt.close()
json.dump(out,open("res_s3.json","w"),indent=1); print(json.dumps(out))
