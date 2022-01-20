### Aggregator in Python using AIOHTTP.

- The main task of the aggregator is to collect information from the specified Web resources and display it in one place and in a convinient form. The resource is the URL address of the page the user is interested in.
- This aggregator collects information about the weather in the city of interested to the user.
- The task of the handler is to get from the HTML responce only the data that the user needs in a format convinient for displaying in the aggregator. The aggregated and cleaned data is displayed on the page.
- The aggregator stores the results of collecting information from sources in the database. This aggregator uses MongoDB.
- Proccesing of information from sources occurs in parallel using coroutines. 
