import pymysql
import requests
import multiprocessing

#Collecte des coordonnées géographiques
#Connection à la BDD
conn = pymysql.connect(
    host='35.205.247.73',
    user='tech-challenge',
    password='password',
    database='dataengineer'
)
cur = conn.cursor()
cur.execute('SELECT * FROM address')
rows = cur.fetchall()

#Récupération des addresses
out = []
for r in rows:
    r_id = r[0]
    r_addr = r[1]
    r_city = r[2]
    r_post = r[3]
    addr_tuple = (r_id,r_addr,r_city,r_post)
    out.append(addr_tuple)

#Requete API
def req_coord(payload):
    r_id = payload[0]
    r_addr = payload[1]
    r_city = payload[2]
    r_post = payload[3]
    url = f"https://nominatim.openstreetmap.org/search?street={r_addr}&city={r_city}&postalcode={r_post}&format=json"
    r = requests.get(url)
    try:
        result = r.json()
        result = result[0]
        lon = result["lon"]
        lat = result["lat"]
        return (r_id,lon,lat)
    except:
        pass

#Requete des coordonnées
sql_payloads = []
for p in out:
    c = req_coord(p)
    sql_payloads.append(c)

#Ajout des nouvelles colonnes
cur.execute("ALTER TABLE address ADD longitude VARCHAR(32) ")
cur.execute("ALTER TABLE address ADD latitude VARCHAR(32) ")

#Remplissage des nouvelles colonnes
for p in sql_payloads:
    try:
        p_id = p[0]
        lon  = p[1]
        lat  = p[2]
        cur.execute(f"UPDATE address SET longitude = '{lon}',latitude  = '{lat}' WHERE address_id = {p_id}")
        conn.commit()
    except:
        pass

