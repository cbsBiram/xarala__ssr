from datetime import datetime, date


date_fin = date(2019, 10, 6)
date_du_jour = date.today()
jour_restant = date_fin - date_du_jour
user_assurance = "SELECT * FROM table"

trois_ou_moins = []

print("Avent ", trois_ou_moins)
filter_days = int(input("Entrez une date"))

for assurance in user_assurance:
    if (assurance.get("date") - date_du_jour).days == filter_days:
        trois_ou_moins.append(assurance)

print("type", type(trois_ou_moins))
