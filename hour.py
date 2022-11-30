from datetime import date, timedelta, datetime
m2 = '3PM'
in_time = datetime.strptime(m2, "%I%p")
out_time = datetime.strftime(in_time, "%H:%M")
print(out_time)