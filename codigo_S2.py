import math, json
# Red carretera simplificada (centro de Veracruz y Puebla). Coordenadas aproximadas (lat, lon).
CIUDADES = {
 "Xalapa":(19.5438,-96.9102), "Coatepec":(19.4511,-96.9606), "Xico":(19.4170,-97.0100),
 "Veracruz":(19.1738,-96.1342), "Cardel":(19.3600,-96.3700), "Cordoba":(18.8847,-96.9261),
 "Orizaba":(18.8500,-97.1000), "Perote":(19.5614,-97.2433), "Puebla":(19.0414,-98.2063),
 "CDMX":(19.4326,-99.1332), "Tehuacan":(18.4667,-97.3929), "Poza Rica":(20.5331,-97.4592),
 "Martinez de la Torre":(20.0667,-97.0500), "Tuxpan":(20.9500,-97.4000), "Tlaxcala":(19.3139,-98.2404),
}
def hav(a,b):
    R=6371.0
    la1,lo1=map(math.radians,a); la2,lo2=map(math.radians,b)
    d=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(d))
CIRC=1.25  # factor de circuidad carretera/recta (supuesto)
def dist_carretera(a,b): return CIRC*hav(CIUDADES[a],CIUDADES[b])
AR=[("Xico","Coatepec"),("Coatepec","Xalapa"),("Xalapa","Perote"),("Xalapa","Cardel"),("Cardel","Veracruz"),
    ("Veracruz","Cordoba"),("Cordoba","Orizaba"),("Orizaba","Tehuacan"),("Tehuacan","Puebla"),("Perote","Puebla"),
    ("Puebla","CDMX"),("Puebla","Tlaxcala"),("Tlaxcala","CDMX"),("Xalapa","Martinez de la Torre"),
    ("Martinez de la Torre","Poza Rica"),("Poza Rica","Tuxpan"),("Cardel","Martinez de la Torre"),
    ("Xico","Perote"),("Cordoba","Xalapa"),("Orizaba","Puebla"),("Xico","Cordoba")]
