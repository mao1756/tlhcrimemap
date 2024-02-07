# Experiment Data Analyis Ideas.

- See https://developers.arcgis.com/python/samples/crime-analysis-and-clustering-using-geoanalytics-and-pyspark/#Use-Spark-Dataframe-and-Run-Python-Script . Although this page is for arcgis, ideas should be applicable to our data. Do something similar to this page.

# Details

- Plot a bar chart for types of reports (Community Policing, Theft, etc.)
- Location of the reports. See "LOCATION_TEXT" column.
- Location of reports for specific category, such as where theft commonly occurs
- Given a coordinate, find out to which city block it belongs. Then, use that information to plot a bar chart for frequency of crimes per block.
- Plot the crime disribution by the hour/day.
- Do the k-means clustering for k=15-20 using the coordinates of crime, and visualize the result.
