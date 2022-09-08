from datetime import date, datetime

print(datetime.strptime(str(date.today()),'%Y-%m-%d').strftime('%d-%m-%Y'))
