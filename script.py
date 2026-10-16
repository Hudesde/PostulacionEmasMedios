import requests
from datetime import datetime, timedelta, timezone

def check_wp_sites(sites):
    failed = []
    limit_time = datetime.now(timezone.utc) - timedelta(hours=24)
    
    for site in sites:
        try:
            api_url = f"{site.rstrip('/')}/wp-json/wp/v2/posts?per_page=1"
            res = requests.get(api_url, timeout=10)
            res.raise_for_status()
            posts = res.json()
            
            if not posts:
                failed.append(f"{site} -> Cero posts encontrados.")
                continue
                
            last_date = datetime.fromisoformat(posts[0]['date_gmt']).replace(tzinfo=timezone.utc)
            if last_date < limit_time:
                failed.append(f"{site} -> Última nota tiene más de 24h ({last_date.date()}).")
                
        except requests.exceptions.RequestException as e:
            failed.append(f"{site} -> Falla de conexión o HTTP error: {e}")
            
    return failed

if __name__ == "__main__":
    wp_sites = [
        "https://ejemplo1.com",
        "https://ejemplo2.com"
    ]
    
    fallos = check_wp_sites(wp_sites)
    print("=== SITIOS QUE FALLARON ===")
    for f in fallos:
        print(f)