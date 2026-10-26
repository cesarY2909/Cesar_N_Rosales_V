import networkx as nx, matplotlib.pyplot as plt, json, math
from common import *
res={}
# --- Problema 1: jarras de agua (4 L y 3 L) ---
CAP=(4,3)
def sucesores(e):
    a,b=e; s=set()
    s|={(CAP[0],b),(a,CAP[1]),(0,b),(a,0)}
    t=min(a,CAP[1]-b); s.add((a-t,b+t))
    t=min(b,CAP[0]-a); s.add((a+t,b-t))
    s.discard(e); return s
G=nx.DiGraph(); pend=[(0,0)]; vis={(0,0)}
while pend:
    e=pend.pop()
    for s in sucesores(e):
        G.add_edge(e,s,weight=1)
        if s not in vis: vis.add(s); pend.append(s)
metas=[e for e in G if e[0]==2]
ruta=min((nx.shortest_path(G,(0,0),m) for m in metas),key=len)
res["jarras"]={"estados":G.number_of_nodes(),"transiciones":G.number_of_edges(),"ruta":[list(x) for x in ruta],
  "pasos":len(ruta)-1,"ramif_prom":round(G.number_of_edges()/G.number_of_nodes(),2),"ramif_max":max(d for _,d in G.out_degree())}
pos=nx.circular_layout(G); plt.figure(figsize=(7,6))
nx.draw_networkx(G,pos,node_size=650,font_size=7,node_color="#dbe7ff",arrows=True,edge_color="#999")
ar=list(zip(ruta,ruta[1:])); nx.draw_networkx_edges(G,pos,edgelist=ar,edge_color="red",width=2.5)
nx.draw_networkx_nodes(G,pos,nodelist=ruta,node_color="#ffd0d0",node_size=650)
plt.title("Espacio de estados: jarras 4 L y 3 L (ruta solución en rojo)"); plt.axis("off")
plt.savefig("fig/s2_jarras.png",dpi=160,bbox_inches="tight"); plt.close()
# --- Problema 2: rutas entre ciudades ---
H=nx.Graph()
for u,v in AR: H.add_edge(u,v,weight=round(dist_carretera(u,v),1))
rt=nx.dijkstra_path(H,"Xico","CDMX",weight="weight"); costo=nx.dijkstra_path_length(H,"Xico","CDMX")
res["rutas"]={"nodos":H.number_of_nodes(),"aristas":H.number_of_edges(),"ruta":rt,"km":round(costo,1),"grado_max":max(d for _,d in H.degree())}
lay={c:(CIUDADES[c][1],CIUDADES[c][0]) for c in CIUDADES}
plt.figure(figsize=(9,6.5)); nx.draw_networkx(H,lay,node_size=500,font_size=7,node_color="#e5f5e0")
nx.draw_networkx_edge_labels(H,lay,edge_labels={(u,v):d["weight"] for u,v,d in H.edges(data=True)},font_size=5)
ar=list(zip(rt,rt[1:])); nx.draw_networkx_edges(H,lay,edgelist=ar,edge_color="red",width=2.5)
plt.title("Grafo ponderado de carreteras (km aprox.) — ruta Xico→CDMX en rojo"); plt.axis("off")
plt.savefig("fig/s2_rutas.png",dpi=160,bbox_inches="tight"); plt.close()
json.dump(res,open("res_s2.json","w"),indent=1,ensure_ascii=False); print(json.dumps(res,ensure_ascii=False))
