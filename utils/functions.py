from utils import variables_layouts as va_lay

def progress_bar(_type, origin, destination, industry):
    if _type and origin and destination and industry:
        return 100
    elif _type and origin and destination:
        return 75
    elif _type and origin:
        return 50
    elif _type:
        return 25
    else:
        return 0
    
def progress_bar2(destination, industry):
    if destination and industry:
        return 100
    elif destination:
        return 50
    else:
        return 0
    
def progress_bar3(origin, destination, industry):
    if destination and industry and origin:
        return 100
    elif destination and origin:
        return 66
    elif origin:
        return 33
    else:
        return 0
    

def find_top_5(totals, industry, dates):
    totals['mean'] = totals[dates].mean(axis=1)
    totals['sum'] = totals[dates].sum(axis=1)
    
    totals = totals[totals['industry'] == industry]
    totals = totals.sort_values(['sum', 'mean'], ascending=False)

    destinations = totals.head(5)['destination'].unique()
    suggestions = []

    for des in destinations:
        try:
            suggestions.append(va_lay.low_export_frequent[des][industry])
        except:
            suggestions.append([])


    return destinations, suggestions