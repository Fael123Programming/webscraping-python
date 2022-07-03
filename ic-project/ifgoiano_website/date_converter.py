from datetime import datetime


class DateConverter:

    @staticmethod
    def convert(date_string: str) -> datetime:
        def get_month_number(month: str) -> int:
            match month.lower():
                case 'janeiro':
                    return 1
                case 'fevereiro':
                    return 2
                case 'março':
                    return 3
                case 'abril':
                    return 4
                case 'maio':
                    return 5
                case 'junho':
                    return 6
                case 'julho':
                    return 7
                case 'agosto':
                    return 8
                case 'setembro':
                    return 9
                case 'outubro':
                    return 10
                case 'novembro':
                    return 11
                case 'dezembro':
                    return 12
                case _:
                    return -1
        split_data = date_string.replace(',', '').replace(':', '').replace(' de', '').split(' ')
        date = dict()
        for i in split_data:
            if i.isdigit():
                i_int = int(i)
                if i_int <= 31:
                    attr = 'day'
                else:
                    attr = 'year'
                date[attr] = i_int
            else:
                month_number = get_month_number(i)
                if month_number != -1:
                    date['month'] = month_number
                else:
                    hour = ''
                    minute = ''
                    h_found = False
                    for j in i:
                        if j == 'h':
                            h_found = True
                            continue
                        if h_found:
                            minute += j
                        else:
                            hour += j
                    if hour.isdigit():
                        date['hour'] = int(hour)
                    if minute.isdigit():
                        date['minute'] = int(minute)
        return datetime(date['year'], date['month'], date['day'], date['hour'], date['minute'])
