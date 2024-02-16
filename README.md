# Trade Canada
Visualize and analyze the data that is gathered from [ic.gc.ca](https://www.ic.gc.ca/app/scr/tdst/tdo/crtr.html?reportType=TI&grouped=INDIVIDUAL&searchType=BL&timePeriod=24%7cMonthly+Trends&currency=CDN&areaCodes=SCA&naArea=9998&countryList=specific&productType=NAICS&toFromCountry=CDN&hSelectedCodes=%7c111140&changeCriteria=true) website.
The purpose of this repo is to visualize the trade data and suggest best periods and best destinations for make trades in different industries.
The application is developed using **Plotly Dash** and it has three tabs which are Graph, Suggestion 1, Suggestion 2
## Graph Tab:
By selecting the origin, the destination and the industry, you will be provided by a graph which shows the trade values of an industry or a product from an origin to a destination

## Suggestion 1 Tab: 
By selecting the destination and the industry, some suggestions for the proper  months for exporting that product or industry to that destination will be given.

This page suggests the best months for making a trade to a destination based on the 
average value of exports of the selected product to the selected destination from all countries 
and Canada. In other word, we consider the average value of exports from all countries to the destination 
within a period of time (e.g., 24 months) and find the periods that the export value is more than the average.
This shows that the demand in this period is higher than other times.


Also, we find the months that the exports from Canada is lower than the average value of exports 
within this period of time. The intersections of these 2 analyses end in final result

It is worth mentionaing that this phenomenon should happen more than 1 time to consider it as a periodic event.

## Suggestion 2 Tab:
By selecting the origin, the destination and the industry, some suggestions for the proper 
months for exporting that product or industry to that destination from the selected origin will be given.

This page suggests the best months for making a trade to a destination based on the 
average value of exports of the selected product to the selected destination from all countries 
and Canada. In other word, we consider the average value of exports from all countries and from Canada to the destination 
within a period of time (e.g., 24 months) and find the months that the export values are more than the average in both terms.
This shows that the demand in these months is higher than other times.

Also, we find the months that the exports from the origin (e.g., Alberta) is lower than the average value of exports 
within this period of time. The intersections of these 3 items end in final result.

It is worth mentionaing that, like suggestion tab 1, this phenomenon should happen more than 1 time to consider it as a periodic event.

### how to run:
```
python visualizer.py
```
<img src="https://github.com/MajidNoorani/Trade-Ca-USA-Visualization/tree/master/assets/app-view.gif" width="800" height="450" />

## codes:
### data cleaning and process
- [data analysis.ipynb](data%20analysis.ipynb)
> 1 - finds the months that the exports from a province to a state is lower than the average  
2 - finds the months that the total exports from the world to a state is higher than the average  
3 - finds the months that are common in both 1 and 2  
4 - checks if it has been heppend in all years.  
>> the final result will be stored in a json file named [rows_with_lower_export_frequent_structured_provinces.json] 

> also there is an another analysis which is as below:  
1 - finds the months that the total exports from the world to a state is higher than the average  
2 - finds the months that the exports from Canada to a state is lower than the average  
3 - find the common months between 1 and 2 and the months that this phenomenon has happened peridically (in all years) 
>> the final result will be stored in a json file named [rows_with_lower_export_frequent_structured.json] 

### main files:

  - [visualizer_NoPredict.py](visualizer_NoPredict.py)
  > visualizes the data in 3 tabs. 
